from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Sport
from .serializers import SportSerializer

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def sport_list(request) -> JsonResponse:

  """
  Récupère une liste de tous les sports.
  Cette vue gère les requêtes GET pour récupérer tous les sports de la base de données.
  Les données sont sérialisées à l'aide de `SportSerializer` et renvoyées sous forme de réponse JSON.
  Les vérifications d'authentification et de permissions sont désactivées pour ce point de terminaison.
  Args:
    request (HttpRequest) : L'objet de la requête HTTP.
  Returns:
    JsonResponse : Une réponse JSON contenant la liste sérialisée des sports avec un code de statut HTTP 200.
  """
  sports = Sport.objects.all().order_by('title')
  serializer = SportSerializer(sports, many=True)
  
  return JsonResponse({'data': serializer.data})