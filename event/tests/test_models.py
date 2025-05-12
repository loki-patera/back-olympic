from datetime import date, time
from django.test import TestCase
from event.models import Competition, Event, Location, Sport

class SportModelTests(TestCase):

  def setUp(self):

    """
    Crée une instance de `Sport` avec des données de test.
    """
    self.sport = Sport.objects.create(
      title="Surf",
      image="sports/surf.jpg"
    )

  def test_sport_str_representation(self):

    """
    Teste la représentation en chaîne de caractères du modèle `Sport` en vérifiant que :
    - La méthode `__str__` du modèle `Sport` retourne la bonne représentation en chaîne.
    """
    self.assertEqual(str(self.sport), "Surf")




class LocationModelTests(TestCase):

  def setUp(self):

    """
    Crée une instance de `Location` avec des données de test.
    """
    self.location = Location.objects.create(
      name="Stade Yves-du-Manoir",
      city="Colombes",
      total_seats=15000
    )

  def test_location_str_representation(self):

    """
    Teste la représentation en chaîne de caractères du modèle `Location` en vérifiant que :
    - La méthode `__str__` du modèle `Location` retourne la bonne représentation en chaîne.
    """
    self.assertEqual(str(self.location), "Stade Yves-du-Manoir (Colombes)")




class EventModelTests(TestCase):

  def setUp(self):

    """
    Crée les instances nécessaires pour tester le modèle `Event`.
    """
    self.sport = Sport.objects.create(
      title="Natation artistique",
      image="sports/natation-artistique.jpg"
    )
    self.location = Location.objects.create(
      name="Centre aquatique olympique",
      city="Saint-Denis",
      total_seats=5000
    )
    self.event = Event.objects.create(
      sport=self.sport,
      location=self.location,
      date=date(2024, 8, 5),
      start_time=time(10, 0),
      end_time=time(12, 0),
      price="50.00"
    )

  def test_event_str_representation(self):

    """
    Teste la représentation en chaîne de caractères du modèle `Event` en vérifiant que :
    - La méthode `__str__` du modèle `Event` retourne la bonne représentation en chaîne.
    """
    expected_str = "Natation artistique | 05/08/2024 (10:00 - 12:00)"
    self.assertEqual(str(self.event), expected_str)
  
  def test_event_available_seats(self):
    
    """
    Teste la propriété `available_seats` du modèle `Event` en vérifiant que :
    - Le nombre de places disponibles est égal au nombre total de places lorsque `booked_seats` est 0.
    """
    self.assertEqual(self.event.available_seats, 5000)




class CompetitionModelTests(TestCase):

  def setUp(self):

    """
    Crée les instances nécessaires pour tester le modèle `Competition`.
    """
    self.sport = Sport.objects.create(
      title="Athlétisme",
      image="sports/athletisme.jpg"
    )
    self.location = Location.objects.create(
      name="Stade de France",
      city="Saint-Denis",
      total_seats=80000
    )
    self.event = Event.objects.create(
      sport=self.sport,
      location=self.location,
      date=date(2024, 7, 28),
      start_time=time(15, 0),
      end_time=time(17, 0),
      price="250.00"
    )
    self.competition = Competition.objects.create(
      description="100 m",
      gender=Competition.Gender.Hommes,
      phase="Finale",
      event=self.event
    )

  def test_competition_str_representation(self):

    """
    Teste la représentation en chaîne de caractères du modèle `Competition` en vérifiant que :
    - La méthode `__str__` du modèle `Competition` retourne la bonne représentation en chaîne.
    """
    expected_str = f"{str(self.event)} | 100 m, Hommes, Finale"
    self.assertEqual(str(self.competition), expected_str)