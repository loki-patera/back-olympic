from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from event.models import Sport

class SportListAPITest(TestCase):

  def setUp(self):

    """
    Configure le client API et créer des sports d'exemple pour les tests.
    """
    # Crée un client API pour effectuer des requêtes sur les points de terminaison de l'API
    self.client = APIClient()
    
    # Crée des exemples de sports dans la base de données pour les tests
    Sport.objects.create(
      title="Football",
      image="images/sports/football.jpg"
    )
    Sport.objects.create(
      title="Basketball",
      image="images/sports/basketball.jpg"
    )
    Sport.objects.create(
      title="Tennis",
      image="images/sports/tennis.jpg"
    )


  def test_sport_list_success(self):

    """
    Teste que le point de terminaison API `sport_list` retourne un code de statut 200 et la liste correcte des sports.
    """
    # Vérifie que le nom de l'URL correspond à la configuration d'URL
    url = reverse('sport_list')
    # Effectue une requête GET sur l'URL
    response = self.client.get(url)

    # Vérifie que le code de statut de la réponse est 200 (OK)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    # Vérifie que la clé 'data' est présente dans la réponse JSON
    self.assertIn('data', response.json())
    # Vérifie que la liste des sports contient le bon nombre d'éléments
    self.assertEqual(len(response.json()['data']), 3)
    # Vérifie que les titres des sports sont corrects
    self.assertEqual(response.json()['data'][0]['title'], "Basketball")
    self.assertEqual(response.json()['data'][1]['title'], "Football")
    self.assertEqual(response.json()['data'][2]['title'], "Tennis")


  def test_sport_list_empty(self):

    """
    Teste que le point de terminaison API `sport_list` retourne une liste vide lorsqu'il n'y a aucun sport dans la base
    de données.
    """
    # Supprime tous les sports existants dans la base de données
    Sport.objects.all().delete()
    # Vérifie que le nom de l'URL correspond à la configuration d'URL
    url = reverse('sport_list')
    # Effectue une requête GET sur l'URL
    response = self.client.get(url)

    # Vérifie que le code de statut de la réponse est 200 (OK)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    # Vérifie que la clé 'data' est présente dans la réponse JSON
    self.assertIn('data', response.json())
    # Vérifie que la liste des sports est vide
    self.assertEqual(len(response.json()['data']), 0)