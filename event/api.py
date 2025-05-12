from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .models import Competition, Event, Sport
from .serializers import CompetitionSerializer, EventSerializer, SportSerializer

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def sport_list(request) -> Response:

  """
  Récupère une liste de toutes les épreuves sportives.

  Args:
    → request (HttpRequest) : L'objet de la requête HTTP.
  Returns:
    → Response : Une réponse JSON contenant la liste sérialisée des épreuves sportives avec un code de statut HTTP 200.
  """
  sports = Sport.objects.all().order_by('title')
  serializer = SportSerializer(sports, many=True)
  return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def event_list(request) -> Response:

  """
  Récupère une liste de tous les événements sportifs.

  Args:
    → request (HttpRequest) : L'objet de la requête HTTP.
  Returns:
    → Response : Une réponse JSON contenant la liste sérialisée des événements sportifs avec un code de statut HTTP 200.
  """
  events = Event.objects.select_related('sport', 'location').order_by('date', 'start_time')
  serializer = EventSerializer(events, many=True)
  
  return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def competition_list_by_event(request, event_id: int) -> Response:

  """
  Récupère une liste de toutes les compétitions associées à un événement sportif spécifique.

  Args:
    → request (HttpRequest) : L'objet de la requête HTTP.
    → event_id (int) : L'identifiant de l'événement sportif.
  Returns:
    → Response : Une réponse JSON contenant la liste sérialisée des compétitions associées à un événement sportif avec un code de statut HTTP 200.
  """
  competitions = Competition.objects.filter(event_id=event_id)
  serializer = CompetitionSerializer(competitions, many=True)
  return Response(serializer.data, status=status.HTTP_200_OK)