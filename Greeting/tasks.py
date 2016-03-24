from django.core.mail import send_mail
from drchronoAPI.api import get_patients_of_doctor, get_doctor_details
from celery.utils.log import get_task_logger
import datetime
from .utils import *
from .models import Greetings
from Birthday_wisher_drchrono.celery_task import app
from UserAuth.views import update_access_token

logger = get_task_logger(__name__)


def format_patient_data(str, patient):
    """
    Returns the string with the patient formatted data
    """
    year = datetime.datetime.now().year
    birth_year = datetime.datetime.strptime(patient['date_of_birth'], '%Y-%m-%d').year
    age = year - birth_year + 1
    return str.format(patient['first_name'], patient['last_name'], ordinal(age))


def is_birthday_today(birth_date):
    """
    returns True if birth_date is of today's month and day
    """
    if birth_date is not None:
        date_obj = datetime.datetime.strptime(birth_date, '%Y-%m-%d')
        today = datetime.datetime.now()
        if today.month == date_obj.month and today.day == date_obj.day:
            return True
    return False


@app.task
def send_greetings():
    """
    A Cron job using celery
    Sends greetings daily in the morning at 07:30 AM(settings)
    Updates access_token if expired
    """
    greetings = Greetings.objects.filter(is_active=True)
    for greeting in greetings:
        access_token = update_access_token(greeting.user)
        doctor_data = get_doctor_details(greeting.doctor, access_token)
        patients = get_patients_of_doctor(greeting.doctor, access_token)
        if greeting.greeting_type == 'e':
            email_subject, email_body = create_greeting(greeting, doctor_data)
            for patient in patients:
                if is_birthday_today(patient['date_of_birth']):
                    patient_email_subject = format_patient_data(email_subject, patient)
                    patient_email_body = format_patient_data(email_body, patient)
                    if patient['email']:
                        send_mail(patient_email_subject, patient_email_body, settings.EMAIL_HOST_USER, [patient['email'], ], fail_silently=True)
                        # send_mail(patient_email_subject, patient_email_body, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=True)

        else:
            sms_message, sms_signature = create_greeting(greeting, doctor_data)
            for patient in patients:
                if is_birthday_today(patient['date_of_birth']):
                    patient_sms_message = format_patient_data(sms_message, patient)
                    patient_sms_signature = format_patient_data(sms_signature, patient)
                    if patient['cell_phone']:
                        send_sms(patient['cell_phone'], patient_sms_message, patient_sms_signature)
