from django.test import TestCase
from event.models import Sport

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