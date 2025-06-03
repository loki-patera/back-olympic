from django.test import TestCase
from unittest.mock import Mock
from user.admin import UserAdmin

class UserAdminTests(TestCase):
    
  def setUp(self):

    """
    Crée une instance de `UserAdmin` avec des objets Mock pour le modèle et le site admin.
    """
    self.user = UserAdmin(model=Mock(), admin_site=Mock())


  def test_account_key_returns_id_person(self):

    """
    Teste que la méthode `account_key` retourne bien la clé du compte de l'utilisateur.
    """
    # Création d'un objet Mock avec un attribut `id_person`
    obj = Mock()
    obj.id_person = "12345"

    # Appel de la méthode `account_key`
    result = self.user.account_key(obj)

    self.assertEqual(result, "12345")