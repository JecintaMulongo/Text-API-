from django.contrib import admin

from django.urls import path
from .views import ContactView, ContactFailView , ContactSuccessView

app_name = 'mailer'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mailer/', ContactView.as_view(), name="mailer"),
    path('success/', ContactSuccessView.as_view(), name="success"),
    path('mailfail/', ContactFailView.as_view(), name="mailfail"),

]
