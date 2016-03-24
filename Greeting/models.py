from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


class Greetings(models.Model):
    GREETING_TYPE = (
        ('e', "EMAIL"),
        ('s', 'SMS'),
    )

    user = models.OneToOneField(User, related_name='Doctor', primary_key=True, verbose_name='doctor')
    doctor = models.IntegerField(unique=True)
    is_active = models.BooleanField(default=False)
    greeting_type = models.CharField(max_length=1, choices=GREETING_TYPE, default=GREETING_TYPE[0][0])
    sms_message = models.CharField(max_length=200, null=True, blank=True, default=
"""
Happy <patient_age> Birthday <patient_first_name> <patient_last_name>

"""
                                   )
    sms_signature = models.CharField(max_length=200, null=True, blank=True, default="Dr. <doctor_first_name> <doctor_last_name>")
    email_subject = models.CharField(max_length=200, null=True, blank=True, default="Happy Birthday")
    email_body = models.TextField(max_length=400, null=True, blank=True, default=
"""
Hi <patient_first_name>,

Wishing you well on your <patient_age> birthday.
May you celebrate many more.

Best Regards,

Dr. <doctor_first_name> <doctor_last_name>
<doctor_job_title>
<doctor_email>
<doctor_cell_phone>
"""
                                  )


class GreetingsAdmin(admin.ModelAdmin):
    exclude = None

admin.site.register(Greetings, GreetingsAdmin)
