import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

from django.conf import  settings
from django.contrib.auth import get_user_model
from django.core.mail import BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.views import View
from django.views.generic import FormView, TemplateView
from django.views.generic.edit import ProcessFormView
from text_classification.classifier import Classifier
from .forms import ContactForm
from django.urls import reverse_lazy
#from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.core import mail
path_to_model = '/home/jecinta/PycharmProjects/TextAPI/static/model/model.h5'

print(path_to_model)
User = get_user_model()



def send_mail(send_from, send_to, subject, text, files=[], server="localhost", ssl=False, username=None, password=None):
    msg = MIMEMultipart('alternative')
    msg.set_charset('utf-8')
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    part = MIMEText(text)
    part.set_charset('utf-8')
    msg.attach(part)
    if ssl:
        smtp = smtplib.SMTP_SSL(server)
    else:
        smtp = smtplib.SMTP(server)
    if username:
        smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

class ContactView(View):
    def get(self, request):
        form = ContactForm()
        context = {'form': form}

        return render(request, 'mailer/mailer.html', context)

    def get_user(self, request):
        form = ContactForm(data=request.POST)
        if form.is_valid():
            email, _, _, _, _ = form.get_info()
            if User.objects.filter(email=email).exists():
                usr = User.objects.get(email=email)
                if usr.is_authenticated:
                    return True
                else:
                    return False
            else:
                print("No user exist with this {} username.".format(email))
                return False

    def post(self, request):
        form = ContactForm(data=request.POST)
        if form.is_valid():
            email_from, email_to, subject, msg, message = form.get_info()
            classifier = Classifier(message, path_to_model)
            prediction = classifier.get_prediction()
            if prediction == 'spam':
                return HttpResponse('Spam Email Failed Sent')
            elif prediction == 'ham':

                try:

                    if self.get_user(request):
                        send_mail( send_from= settings.DEFAULT_FROM_EMAIL,
                                  send_to=settings.RECIPIENT_ADDRESS,text=message,subject=subject)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
        return render(request, 'mailer/success.html', context={})


class ContactSuccessView(TemplateView):
    template_name = 'mailer/success.html'


class ContactFailView(TemplateView):
    template_name = 'mailer/fail.html'
