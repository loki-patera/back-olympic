from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from .models import User
from .serializers import RegisterUserSerializer

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def check_email_exists(request: Request) -> Response:
    
  """
  Vérifie si un utilisateur existe avec l'email donné.

  Args:
    → request (HttpRequest) : L'objet de la requête HTTP contenant l'email à vérifier.
  Returns:
    → Response : Une réponse JSON contenant un booléen indiquant si l'email existe ou non, avec un code de statut HTTP 200.
  """
  email = request.data.get("email")

  exists = User.objects.filter(email=email).exists()
  
  return Response({"exists": exists}, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def register_user(request: Request) -> Response:
    
  """
  Enregistre un nouvel utilisateur avec les données fournies dans la requête.

  Args:
    → request (HttpRequest) : L'objet de la requête HTTP contenant les données de l'utilisateur à enregistrer.
  Returns:
    → Response : Une réponse JSON indiquant si l'enregistrement a réussi ou échoué, avec un code de statut HTTP approprié.
  """
  serializer = RegisterUserSerializer(data=request.data)
  
  if serializer.is_valid():
    serializer.save()
    return Response({"success": True}, status=status.HTTP_201_CREATED)
  
  return Response({"success": False, "errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)