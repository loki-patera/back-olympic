from django.test import TestCase
from offer.models import Offer

class OfferModelTests(TestCase):

  def setUp(self):

    """
    Crée une instance de `Offer` avec des données de test.
    """
    self.offer = Offer.objects.create(
      type="Groupe - 10 adultes",
      number_seats=10,
      discount=20
    )
  
  def test_offer_str_representation(self):
    
    """
    Teste la représentation en chaîne de caractères du modèle `Offer` en vérifiant que :
    - La méthode `__str__` du modèle `Offer` retourne la bonne représentation en chaîne.
    """
    self.assertEqual(str(self.offer), "Groupe - 10 adultes")