from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
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