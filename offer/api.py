from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .models import Offer
from .serializers import OfferSerializer, SeatSerializer

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def number_seats_list(request):
    
  """
  Récupère la liste des valeurs distinctes du nombre de places des offres.

  Args:
    → request (HttpRequest) : L'objet de la requête HTTP.
  Returns:
    → Response : Une liste JSON du nombres de places distincts.
  """
  seats = Offer.objects.values('number_seats').distinct().order_by('number_seats')
  serializer = SeatSerializer(seats, many=True)
  return Response(serializer.data, status=status.HTTP_200_OK)




@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def offer_list(request):
    
  """
  Récupère la liste de toutes les offres.

  Args:
    → request (HttpRequest) : L'objet de la requête HTTP.
  Returns:
    → Response : Une réponse JSON contenant la liste sérialisée des offres avec un code de statut HTTP 200.
  """
  offers = Offer.objects.all().order_by('number_seats', 'discount')
  serializer = OfferSerializer(offers, many=True)
  return Response(serializer.data, status=status.HTTP_200_OK)