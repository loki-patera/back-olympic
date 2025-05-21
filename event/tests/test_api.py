from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from event.models import Competition, Event, Location, Sport
from offer.models import Offer
from offer.serializers import OfferSerializer

class SportListAPITest(TestCase):

  def setUp(self):

    """
    Configure le client API et créer des sports d'exemple pour les tests.
    """
    # Crée un client API pour effectuer des requêtes sur les points de terminaison de l'API
    self.client = APIClient()
    
    # Crée des exemples de sports
    Sport.objects.create(
      title="Football",
      image="sports/football.jpg"
    )
    Sport.objects.create(
      title="Basketball",
      image="sports/basketball.jpg"
    )
    Sport.objects.create(
      title="Tennis",
      image="sports/tennis.jpg"
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

    data = response.json()
    # Vérifie que la liste des sports contient le bon nombre d'éléments
    self.assertEqual(len(data), 3)
    # Vérifie que les titres des sports sont corrects
    self.assertEqual(data[0]['title'], "Basketball")
    self.assertEqual(data[1]['title'], "Football")
    self.assertEqual(data[2]['title'], "Tennis")

  def test_sport_list_empty(self):

    """
    Teste que le point de terminaison API `sport_list` retourne une liste vide lorsqu'il n'y a aucun sport dans la base de données.
    """
    # Supprime tous les sports existants dans la base de données
    Sport.objects.all().delete()
    # Vérifie que le nom de l'URL correspond à la configuration d'URL
    url = reverse('sport_list')
    # Effectue une requête GET sur l'URL
    response = self.client.get(url)

    # Vérifie que le code de statut de la réponse est 200 (OK)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    # Vérifie que la liste des sports est vide
    self.assertEqual(len(response.json()), 0)




class EventListAPITest(TestCase):

  def setUp(self):

    """
    Configure le client API et crée des événements d'exemple pour les tests.
    """
    # Crée un client API pour effectuer des requêtes sur les points de terminaison de l'API
    self.client = APIClient()

    # Crée des exemples de sports et de lieux
    sport = Sport.objects.create(
      title="Football",
      image="sports/football.jpg"
    )
    location = Location.objects.create(
      name="Stade Olympique",
      city="Paris",
      total_seats=50000
    )

    # Crée des exemples d'événements
    Event.objects.create(
      sport=sport,
      location=location,
      date="2025-07-20",
      start_time="15:00:00",
      end_time="17:00:00",
      price="50.00"
    )
    Event.objects.create(
      sport=sport,
      location=location,
      date="2025-07-21",
      start_time="16:00:00",
      end_time="20:00:00",
      price="100.00"
    )

  def test_event_list_success(self):

    """
    Teste que le point de terminaison API `event_list` retourne un code de statut 200
    et la liste correcte des événements.
    """
    # Vérifie que le nom de l'URL correspond à la configuration d'URL
    url = reverse('event_list')
    # Effectue une requête GET sur l'URL
    response = self.client.get(url)

    # Vérifie que le code de statut de la réponse est 200 (OK)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    data = response.json()
    # Vérifie que la liste des événements contient le bon nombre d'éléments
    self.assertEqual(len(data), 2)
    # Vérifie que les détails des événements sont corrects
    self.assertEqual(data[0]['sport']['title'], "Football")
    self.assertEqual(data[0]['location']['name'], "Stade Olympique")
    self.assertEqual(data[0]['date'], "2025-07-20")
    self.assertEqual(data[0]['start_time'], "15:00:00")
    self.assertEqual(data[0]['end_time'], "17:00:00")
    self.assertEqual(data[0]['price'], "50.00")

    self.assertEqual(data[1]['sport']['title'], "Football")
    self.assertEqual(data[1]['location']['name'], "Stade Olympique")
    self.assertEqual(data[1]['date'], "2025-07-21")
    self.assertEqual(data[1]['start_time'], "16:00:00")
    self.assertEqual(data[1]['end_time'], "20:00:00")
    self.assertEqual(data[1]['price'], "100.00")




class CompetitionListByEventAPITest(TestCase):

  def setUp(self):
    
    """
    Configure le client API et crée des compétitions d'exemple pour les tests.
    """
    # Crée un client API pour effectuer des requêtes sur les points de terminaison de l'API
    self.client = APIClient()

    # Crée des exemples de sports, de lieux et d'événements
    sport = Sport.objects.create(
      title="Football",
      image="sports/football.jpg"
    )
    location = Location.objects.create(
      name="Stade Olympique",
      city="Paris",
      total_seats=50000
    )
    event = Event.objects.create(
      sport=sport,
      location=location,
      date="2025-07-20",
      start_time="15:00:00",
      end_time="17:00:00",
      price="50.00"
    )

    # Crée des exemples de compétitions
    Competition.objects.create(
      description="Match 1",
      gender="Hommes",
      phase="Phase 1",
      event=event
    )
    Competition.objects.create(
      description="Match 2",
      gender="Femmes",
      phase="Phase 1",
      event=event
    )

    # Récupère l'ID de l'événement créé pour les tests
    self.event_id = event.id_event

  def test_competition_list_by_event_success(self):

    """
    Teste que le point de terminaison API `competition_list_by_event` retourne un code de statut 200 et la liste correcte des compétitions pour un
    événement donné.
    """
    # Vérifie que le nom de l'URL correspond à la configuration d'URL
    url = reverse('competition_list_by_event', args=[self.event_id])
    # Effectue une requête GET sur l'URL
    response = self.client.get(url)

    # Vérifie que le code de statut de la réponse est 200 (OK)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    data = response.json()
    # Vérifie que la liste des compétitions contient le bon nombre d'éléments
    self.assertEqual(len(data), 2)
    # Vérifie que les détails des compétitions sont corrects
    self.assertEqual(data[0]['description'], "Match 1")
    self.assertEqual(data[1]['description'], "Match 2")




class CartDetailsAPITest(TestCase):

  def setUp(self):

    """
    Configure le client API et crée des événements et des offres d'exemple pour les tests.
    """
    # Crée un client API pour effectuer des requêtes sur les points de terminaison de l'API
    self.client = APIClient()

    # Crée des exemples de sports, de lieux, d'événements et d'offres
    self.sport = Sport.objects.create(
      title="Natation",
      image="sports/natation.jpg"
    )
    self.location = Location.objects.create(
      name="Piscine Olympique",
      city="Marseille",
      total_seats=10000
    )
    self.event = Event.objects.create(
      sport=self.sport,
      location=self.location,
      date="2025-08-01",
      start_time="10:00:00",
      end_time="12:00:00",
      price="30.00"
    )
    self.offer = Offer.objects.create(
      type="Offre Solo",
      number_seats=1,
      discount=2
    )

  def test_cart_details_success(self):

    """
    Teste que le point de terminaison API `cart_details` retourne un code de statut 200 et les détails corrects des événements et des offres.
    """
    # Vérifie que le nom de l'URL correspond à la configuration d'URL
    url = reverse('cart_details')

    #  Crée une liste de données de réservation avec les ID d'événement et d'offre
    payload = [{
      "id_event": self.event.id_event,
      "id_offer": self.offer.id_offer
    }]

    # Effectue une requête POST sur l'URL avec les données de la réservation
    response = self.client.post(url, payload, format='json')

    # Vérifie que le code de statut de la réponse est 200 (OK)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    data = response.json()
    # Vérifie que la liste des détails pour le panier contient le bon nombre d'éléments
    self.assertEqual(len(data), 1)
    # Vérifie que les détails des événements et des offres sont corrects
    self.assertEqual(data[0]['event']['id_event'], self.event.id_event)
    self.assertEqual(data[0]['event']['sport']['title'], self.sport.title)
    self.assertEqual(data[0]['event']['location']['name'], self.location.name)
    self.assertEqual(data[0]['event']['location']['city'], self.location.city)
    self.assertEqual(data[0]['event']['date'], "2025-08-01")
    self.assertEqual(data[0]['event']['start_time'], "10:00:00")
    self.assertEqual(data[0]['event']['end_time'], "12:00:00")
    self.assertEqual(data[0]['event']['price'], "30.00")

    self.assertEqual(data[0]['offer']['id_offer'], self.offer.id_offer)
    self.assertEqual(data[0]['offer']['type'], "Offre Solo")
    self.assertEqual(data[0]['offer']['number_seats'], 1)
    self.assertEqual(data[0]['offer']['discount'], 2)

  def test_cart_details_invalid_ids(self):

    """
    Teste que le point de terminaison API `cart_details` retourne un code de statut 200 et une liste vide lorsque les ID d'événement et d'offre sont
    invalides.
    """
    # Vérifie que le nom de l'URL correspond à la configuration d'URL
    url = reverse('cart_details')

    # Crée une liste de données de réservation avec des ID d'événement et d'offre invalides
    payload = [{
      "id_event": 9999,
      "id_offer": 8888
    }]

    # Effectue une requête POST sur l'URL avec les données de la réservation
    response = self.client.post(url, payload, format='json')

    # Vérifie que le code de statut de la réponse est 200 (OK)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    data = response.json()
    # Vérifie que la liste des détails pour le panier est vide
    self.assertEqual(data, [])

  def test_cart_details_empty_payload(self):

    """
    Teste que le point de terminaison API `cart_details` retourne un code de statut 200 et une liste vide lorsque les ID d'événement et d'offre ne
    sont pas fournis.
    """
    # Vérifie que le nom de l'URL correspond à la configuration d'URL
    url = reverse('cart_details')

    # Crée une liste de données de réservation vide
    payload = []

    # Effectue une requête POST sur l'URL sans données de réservation
    response = self.client.post(url, payload, format='json')

    # Vérifie que le code de statut de la réponse est 200 (OK)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    data = response.json()
    # Vérifie que la liste des détails pour le panier est vide
    self.assertEqual(data, [])