from django.urls import path
from . import api
from . import views

urlpatterns = [
  path('seats', api.number_seats_list, name='number_seats_list'),
  path('offers', api.offer_list, name='offer_list'),
  path('stats', views.stats, name='stats')
]