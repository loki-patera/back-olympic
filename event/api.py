from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Competition, Event, Sport
from .serializers import CompetitionSerializer, EventLightSerializer, EventSerializer, SportSerializer
from offer.models import Offer
from offer.serializers import OfferSerializer

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def sport_list(request: Request) -> Response:

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
def event_list(request: Request) -> Response:

  """
  Récupère une liste de tous les événements sportifs.

  Args:
    → request (HttpRequest) : L'objet de la requête HTTP.
  Returns:
    → Response : Une réponse JSON contenant la liste sérialisée des événements sportifs avec un code de statut HTTP 200.
  """
  events = Event.objects.select_related('sport', 'location').order_by('date', 'start_time', 'end_time')
  serializer = EventSerializer(events, many=True)
  
  return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def competition_list_by_event(request: Request, event_id: int) -> Response:

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


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def cart_details(request: Request) -> Response:

  """
  Récupère les détails des événements et des offres associés à une liste d'articles dans le panier.

  Args:
    → request (HttpRequest) : L'objet de la requête HTTP contenant les articles du panier.
  Returns:
    → Response : Une réponse JSON contenant les détails des événements et des offres associés aux articles du panier avec un code de statut HTTP 200.
  """
  items = request.data
  result = []

  for item in items:

    try:
      event = Event.objects.select_related('sport', 'location').get(id_event=item['id_event'])
      offer = Offer.objects.get(id_offer=item['id_offer'])
    
    except (Event.DoesNotExist, Offer.DoesNotExist):
      continue

    result.append({
      'event': EventLightSerializer(event).data,
      'offer': OfferSerializer(offer).data
    })

    result.sort(
      key=lambda x: (
        x['event']['date'],
        x['event']['start_time'],
        x['event']['end_time']
      )
    )
  
  return Response(result, status=status.HTTP_200_OK)