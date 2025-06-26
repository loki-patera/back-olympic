from django.urls import path
from . import api

urlpatterns = [
  path('payment', api.process_payment, name='process_payment')
]