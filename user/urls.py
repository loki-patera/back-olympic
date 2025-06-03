from django.urls import path
from . import api

urlpatterns = [
  path('check-email', api.check_email_exists, name='check_email_exists'),
  path('register', api.register_user, name='register_user')
]