from rest_framework import serializers
from .models import Offer

class SeatSerializer(serializers.ModelSerializer):

  class Meta:
    model = Offer
    fields = (
      'number_seats',
    )




class OfferSerializer(serializers.ModelSerializer):

  class Meta:
    model = Offer
    fields = (
      'id_offer',
      'type',
      'number_seats',
      'discount'
    )