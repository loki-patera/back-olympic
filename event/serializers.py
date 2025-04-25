from rest_framework import serializers
from .models import Sport

class SportSerializer(serializers.ModelSerializer):

  class Meta:
    model = Sport
    fields = (
      'id_sport',
      'title',
      'image_url'
    )