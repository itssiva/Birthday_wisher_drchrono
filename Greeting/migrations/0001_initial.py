# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Greetings',
            fields=[
                ('user', models.OneToOneField(related_name='Doctor', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name=b'doctor')),
                ('doctor', models.IntegerField(unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('greeting_type', models.CharField(default=b'e', max_length=1, choices=[(b'e', b'EMAIL'), (b's', b'SMS')])),
                ('sms_message', models.CharField(default=b'\nHappy <patient_age> Birthday <patient_first_name> <patient_last_name>\n\n', max_length=200, null=True, blank=True)),
                ('sms_signature', models.CharField(default=b'Dr. <doctor_first_name> <doctor_last_name>', max_length=200, null=True, blank=True)),
                ('email_subject', models.CharField(default=b'Happy Birthday', max_length=200, null=True, blank=True)),
                ('email_body', models.TextField(default=b'\nHi <patient_first_name>,\n\nWishing you well on your <patient_age> birthday.\nMay you celebrate many more.\n\nBest Regards,\n\nDr. <doctor_first_name> <doctor_last_name>\n<doctor_job_title>\n<doctor_email>\n<doctor_cell_phone>\n', max_length=400, null=True, blank=True)),
            ],
        ),
    ]
