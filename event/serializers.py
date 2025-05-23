from rest_framework import serializers
from .models import Competition, Event, Location, Sport

class SportSerializer(serializers.ModelSerializer):

  class Meta:
    model = Sport
    fields = (
      'id_sport',
      'title',
      'image'
    )


class SportLightSerializer(serializers.ModelSerializer):
  class Meta:
    model = Sport
    fields = (
      'title',
    )


class LocationSerializer(serializers.ModelSerializer):

  class Meta:
    model = Location
    fields = (
      'id_location',
      'name',
      'city',
      'total_seats'
    )


class LocationLightSerializer(serializers.ModelSerializer):
  class Meta:
    model = Location
    fields = (
      'name',
      'city'
    )


class EventSerializer(serializers.ModelSerializer):

  sport = SportSerializer()
  location = LocationSerializer()

  class Meta:
    model = Event
    fields = (
      'id_event',
      'sport',
      'location',
      'date',
      'start_time',
      'end_time',
      'price',
      'available_seats'
    )


class EventLightSerializer(serializers.ModelSerializer):
  sport = SportLightSerializer()
  location = LocationLightSerializer()

  class Meta:
    model = Event
    fields = (
      'id_event',
      'sport',
      'location',
      'date',
      'start_time',
      'end_time',
      'price'
    )


class CompetitionSerializer(serializers.ModelSerializer):

  class Meta:
    model = Competition
    fields = (
      'id_competition',
      'description',
      'gender',
      'phase',
      'event'
    )