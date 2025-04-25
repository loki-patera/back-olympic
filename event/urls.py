from django.urls import path
from . import api

urlpatterns = [
  path('sports', api.sport_list, name='sport_list')
]