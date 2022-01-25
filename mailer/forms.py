import json

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, BadHeaderError
from text_classification.classifier import Classifier
from django.http import HttpResponse
from django.shortcuts import redirect, render

path_to_model = '/home/jecinta/PycharmProjects/TextAPI/static/model/model.h5'

print(path_to_model)
User = get_user_model()


class ContactForm(forms.Form):
    email_from = forms.ModelChoiceField(queryset=User.objects.all(), empty_label=None)
    sent_to = forms.ModelChoiceField(queryset=User.objects.all(), empty_label=None)
    inquiry = forms.CharField(max_length=70)
    message = forms.CharField(widget=forms.Textarea)

    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
        cl_data = super().clean()
        email_from = cl_data.get('email_from')
        email_to = cl_data.get('sent_to')
        subject = cl_data.get('inquiry')
        message = cl_data.get('message')

        msg = f'{email_from} with email to {email_to} said:{message}'

        msg += f'\n"{subject}"\n\n'
        msg += cl_data.get('message')

        return email_from, email_to, subject, msg, message

