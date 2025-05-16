from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from offer.models import Offer

class NumberSeatsListAPITest(TestCase):

  def setUp(self):

    """
    Configure le client API et crée des offres d'exemple pour les tests.
    """
    # Crée un client API pour effectuer des requêtes sur les points de terminaison de l'API
    self.client = APIClient()

    # Crée des exemples d'offres
    Offer.objects.create(
      type="Duo 2 adultes",
      number_seats=2,
      discount=4
    )
    Offer.objects.create(
      type="Quatuor 4 adultes",
      number_seats=4,
      discount=8
    )
    Offer.objects.create(
      type="Duo 1 adulte / 1 enfant",
      number_seats=2,
      discount=14
    )

  def test_number_seats_list_success(self):

    """
    Teste que le point de terminaison API `number_seats_list` retourne un code de statut 200 et la liste correcte des valeurs distinctes du nombre de
    places.
    """
    # Vérifie que le nom de l'URL correspond à la configuration d'URL
    url = reverse('number_seats_list')
    # Effectue une requête GET sur l'URL
    response = self.client.get(url)
    
    # Vérifie que le code de statut de la réponse est 200 (OK)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    data = response.json()
    # Vérifie que la liste des valeurs distinctes du nombre de places contient le bon nombre d'éléments
    self.assertEqual(len(data), 2)

    # Vérifie que les valeurs distinctes du nombre de places sont correctes
    self.assertEqual(data[0]['number_seats'], 2)
    self.assertEqual(data[1]['number_seats'], 4)




class OfferListAPITest(TestCase):

  def setUp(self):

    """
    Configure le client API et crée des offres d'exemple pour les tests.
    """
    # Crée un client API pour effectuer des requêtes sur les points de terminaison de l'API
    self.client = APIClient()

    # Crée des exemples d'offres
    Offer.objects.create(
      type="Duo 2 adultes",
      number_seats=2,
      discount=4
    )
    Offer.objects.create(
      type="Quatuor 4 adultes",
      number_seats=4,
      discount=8
    )
    Offer.objects.create(
      type="Duo 1 adulte / 1 enfant",
      number_seats=2,
      discount=14
    )

  def test_offer_list_success(self):

    """
    Teste que le point de terminaison API `offer_list` retourne un code de statut 200 et la liste correcte des offres.
    """
    # Vérifie que le nom de l'URL correspond à la configuration d'URL
    url = reverse('offer_list')
    # Effectue une requête GET sur l'URL
    response = self.client.get(url)

    # Vérifie que le code de statut de la réponse est 200 (OK)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    data = response.json()
    # Vérifie que la liste des offres contient le bon nombre d'éléments
    self.assertEqual(len(data), 3)

    # Vérifie que les détails des offres sont corrects et l'ordre appliqué (par number_seats, puis discount)
    self.assertEqual(data[0]['type'], "Duo 2 adultes")
    self.assertEqual(data[0]['number_seats'], 2)
    self.assertEqual(data[0]['discount'], 4)

    self.assertEqual(data[1]['type'], "Duo 1 adulte / 1 enfant")
    self.assertEqual(data[1]['number_seats'], 2)
    self.assertEqual(data[1]['discount'], 14)

    self.assertEqual(data[2]['type'], "Quatuor 4 adultes")
    self.assertEqual(data[2]['number_seats'], 4)
    self.assertEqual(data[2]['discount'], 8)