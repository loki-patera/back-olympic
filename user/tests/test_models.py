from django.test import TestCase
from django.contrib.auth import get_user_model
from user.models import Person

# Utilisation du modèle personnalisé
User = get_user_model()

class AccountUserManagerTests(TestCase):

  def setUp(self):

    """
    Configure les données de test pour l'utilisateur et le superutilisateur.
    """
    
    self.user_data = {
      "email": "testuser@example.com",
      "password": "testpassword123",
      "firstname": "John",
      "lastname": "Doe",
      "date_of_birth": "1990-01-01",
      "country": "Belgique"
    }
    self.superuser_data = {
      "email": "admin@example.com",
      "password": "adminpassword123",
      "firstname": "José",
      "lastname": "Admin",
      "date_of_birth": "1985-01-01",
      "country": "France"
    }

  def test_create_user_with_valid_email(self):

    """
    Teste la création d'un utilisateur avec une adresse email valide et vérifie les points suivants :
    - L'email de l'utilisateur correspond à l'email fourni dans `self.user_data`.
    - L'utilisateur n'a pas de privilèges de staff (`is_staff` défini à False).
    - L'utilisateur n'a pas de privilèges de superutilisateur (`is_superuser` défini à False).
    - Le mot de passe de l'utilisateur est correctement défini et peut être vérifié.
    """

    user = User.objects.create_user(**self.user_data)

    self.assertEqual(user.email, self.user_data["email"])
    self.assertFalse(user.is_staff)
    self.assertFalse(user.is_superuser)
    self.assertTrue(user.check_password(self.user_data["password"]))

  def test_create_user_without_email(self):

    """
    Teste que la création d'un utilisateur sans adresse email soulève une ValueError et vérifie le point suivant :
    - Le message d'erreur attendu est : "Vous n'avez pas donné une adresse email valide".
    """

    self.user_data["email"] = None

    with self.assertRaises(ValueError) as context:
      User.objects.create_user(**self.user_data)
    
    self.assertEqual(str(context.exception), "Vous n'avez pas donné une adresse email valide")

  def test_create_superuser_with_valid_email(self):

    """
    Teste la création d'un superutilisateur avec une adresse email valide et vérifie les points suivants :
    - L'email du superutilisateur correspond à l'email fourni dans `self.superuser_data`.
    - Le superutilisateur a le privilège de staff (`is_staff` défini à True).
    - Le superutilisateur a le privilège de superutilisateur (`is_superuser` défini à True).
    - Le mot de passe du superutilisateur est correctement défini et peut être vérifié.
    """

    superuser = User.objects.create_superuser(**self.superuser_data)
    
    self.assertEqual(superuser.email, self.superuser_data["email"])
    self.assertTrue(superuser.is_staff)
    self.assertTrue(superuser.is_superuser)
    self.assertTrue(superuser.check_password(self.superuser_data["password"]))


class PersonModelTests(TestCase):

  def setUp(self):

    """
    Configure les données de test pour le modèle Person.
    """

    self.person_data = {
      "firstname": "Sylvie",
      "lastname": "Dupond",
      "date_of_birth": "1994-10-16",
      "country": "France"
    }
    self.person = Person.objects.create(**self.person_data)

  def test_person_str_representation(self):

    """
    Teste la représentation sous forme de chaîne du modèle Person en vérifiant que :
    - La chaîne de caractère attendu correspond au format "firstname lastname".
    """

    expected_str = f"{self.person_data['firstname']} {self.person_data['lastname']}"
    self.assertEqual(str(self.person), expected_str)