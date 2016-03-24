from drchronoAPI.api import get_doctor_details
import re
from twilio.rest import TwilioRestClient
from django.conf import settings


def ordinal(age):
    """
    converts a number into word representation 
    Ex: 1- 1st, 2- 2nd, 3-3rd, ...11- 11th, ....
    """
    temp_age = age
    while(temp_age>100):
        temp_age = temp_age/10
    if 4 <= temp_age <= 20 or 24 <= temp_age <= 30:
       suffix = "th"
    else:
       suffix = ["st", "nd", "rd"][temp_age % 10 - 1]
    return str(age)+suffix


def send_sms(to_number, sms_message, sms_signature):
    """
    send a SMS from service to to_number using a gateway(Twilio)
    """
    client = TwilioRestClient(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
    print "SENDING To "+to_number
    client.messages.create(to=to_number, from_=settings.TWILIO_NUMBER, body=sms_message+sms_signature,)


def format_greeting(text, doctor):
    """
    takes the text and replaces the tags of doctor with the actual doctor's data,
    replcaes patients data with indices for further formatting
    """
    PATTERN = '<[^<>]*>'
    patient_variables = ['<patient_first_name>', '<patient_last_name>', '<patient_age>']
    doctor_varibales= {'<doctor_first_name>': doctor['first_name'],
                        '<doctor_last_name>': doctor['last_name'],
                        '<doctor_email>': doctor['email'],
                        '<doctor_specialty>': doctor['specialty'],
                        '<doctor_job_title>': doctor['job_title'],
                        '<doctor_suffix>': doctor['suffix'],
                        '<doctor_website>': doctor['website'],
                        '<doctor_home_phone>': doctor['home_phone'],
                        '<doctor_office_phone>': doctor['office_phone'],
                        '<doctor_cell_phone>': doctor['cell_phone']
    }
    for match in re.findall(PATTERN, text):
        if match in patient_variables:
            index = patient_variables.index(match)
            text = text.replace(match, '{'+str(index)+'}')
        elif match in doctor_varibales:
            text = text.replace(match, doctor_varibales[match])
    return text


def create_greeting(greeting, doctor_details):
    """
    Takes a greeting object and doctor's details and returns the formatted messages based on greeting type.
    """

    if greeting.greeting_type == 'e':
        email_subject = format_greeting(greeting.email_subject, doctor_details)
        email_body = format_greeting(greeting.email_body, doctor_details)
        return email_subject, email_body
    else:
        sms_message = format_greeting(greeting.sms_message, doctor_details)
        sms_signature = format_greeting(greeting.sms_signature, doctor_details)
        return sms_message, sms_signature
