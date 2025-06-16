from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.test import TestCase
from user.models import User

class CheckEmailExistsAPITest(TestCase):

  def setUp(self):

    """
    Configure les données de test pour l'API de vérification d'email.
    """
    # Initialisation du client API et de l'URL
    self.client = APIClient()
    self.url = reverse('check_email_exists')

    # Création d'un utilisateur existant
    self.user = User.objects.create_user(
      email="test@example.com",
      password="MotdepasseValide123!",
      firstname="Jean",
      lastname="Dupont",
      date_of_birth="1990-01-01",
      country="France"
    )

  def test_email_exists_true(self):

    """
    Teste que l'API retourne exists=True pour un email existant.
    """
    response = self.client.post(self.url, {"email": "test@example.com"}, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.json(), {"exists": True})

  def test_email_exists_false(self):

    """
    Teste que l'API retourne exists=False pour un email inexistant.
    """
    response = self.client.post(self.url, {"email": "nouveau@example.com"}, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.json(), {"exists": False})




class RegisterUserAPITest(TestCase):

  def setUp(self):
    
    """
    Configure les données de test pour l'API d'enregistrement d'utilisateur.
    """
    self.client = APIClient()
    self.url = reverse('register_user')

  def test_register_user_success(self):
      
    """
    Teste l'enregistrement d'un utilisateur avec des données valides.
    """
    data = {
      "email": "alice@example.com",
      "password": "MotdepasseValide123!",
      "firstname": "Alice",
      "lastname": "Martin",
      "date_of_birth": "1990-05-10",
      "country": "France"
    }
    response = self.client.post(self.url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.json(), {"success": True})
    self.assertTrue(User.objects.filter(email="alice@example.com").exists())

  def test_register_user_invalid_country(self):
      
    """
    Teste l'enregistrement échoué avec un pays invalide.
    """
    data = {
      "email": "alice@example.com",
      "password": "MotdepasseValide123!",
      "firstname": "Alice",
      "lastname": "Martin",
      "date_of_birth": "1990-05-10",
      "country": "Atlantide"  # Pays fictif pour le test
    }
    response = self.client.post(self.url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertFalse(response.json()["success"])
    self.assertIn("country", response.json()["errors"])




class MeAPITest(TestCase):

  def setUp(self):

    """
    Configure les données de test pour l'API de récupération des informations utilisateur.
    """
    self.client = APIClient()
    self.user = User.objects.create_user(
      email="meuser@example.com",
      password="MotdepasseValide123!",
      firstname="Marie",
      lastname="Curie",
      date_of_birth="1980-01-01",
      country="France"
    )
    self.url = reverse('me')
    refresh = RefreshToken.for_user(self.user)
    self.access_token = str(refresh.access_token)

  def test_me_authenticated(self):
      
    """
    Teste que l'utilisateur authentifié reçoit ses informations.
    """
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), {
      "firstname": "Marie",
      "lastname": "Curie"
    })

  def test_me_unauthenticated(self):
      
    """
    Teste que l'accès sans authentification est refusé.
    """
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 401)




class LogoutUserAPITest(TestCase):

  def setUp(self):

    """
    Configure les données de test pour l'API de déconnexion d'utilisateur.
    """
    self.client = APIClient()
    self.user = User.objects.create_user(
      email="logoutuser@example.com",
      password="MotdepasseValide123!",
      firstname="Paul",
      lastname="Valéry",
      date_of_birth="1985-01-01",
      country="France"
    )
    self.url = reverse('logout_user')
    refresh = RefreshToken.for_user(self.user)
    self.access_token = str(refresh.access_token)

  def test_logout_authenticated(self):

    """
    Teste que l'utilisateur authentifié peut se déconnecter.
    """
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
    response = self.client.post(self.url)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), {"success": True})

  def test_logout_unauthenticated(self):

    """
    Teste que l'accès sans authentification est refusé.
    """
    response = self.client.post(self.url)
    self.assertEqual(response.status_code, 401)