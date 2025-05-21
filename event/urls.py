from django.urls import path
from . import api

urlpatterns = [
  path('sports', api.sport_list, name='sport_list'),
  path('events', api.event_list, name='event_list'),
  path('competitions/<int:event_id>', api.competition_list_by_event, name='competition_list_by_event'),
  path('cart', api.cart_details, name='cart_details')
]