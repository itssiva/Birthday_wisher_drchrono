from django import forms
from .models import Greetings


class GreetingForm(forms.ModelForm):
    class Meta:
        model = Greetings
        exclude = ['user', 'is_active', 'doctor_id']
