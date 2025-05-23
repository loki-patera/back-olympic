from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .models import User

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def check_email_exists(request):
    
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