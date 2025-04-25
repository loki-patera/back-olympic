from django.test import TestCase, RequestFactory
from django.contrib import admin
from django.contrib.auth import get_user_model
from user.admin import UserAdmin

class UserAdminTests(TestCase):
    
  def setUp(self):

    """
    Configure l'environnement de test pour les tests d'administration des utilisateurs.
    """

    # Utilisation du modèle personnalisé
    User = get_user_model()
    
    self.superuser = User.objects.create_superuser(
      email="superuser@example.com",
      password="superuserpassword123",
      firstname="John",
      lastname="Doe",
      date_of_birth="1990-01-01",
      country="Belgique"
    )
    self.admin = User.objects.create_user(
      email="admin@example.com",
      password="adminpassword123",
      firstname="José",
      lastname="Admin",
      date_of_birth="1985-01-01",
      country="France"
    )
    
    # Initialise une instance de `RequestFactory` pour simulation de requêtes HTTP
    self.factory = RequestFactory()
    
    # Initialise une instance `UserAdmin` pour tester les fonctionnalités d'administration 
    self.user_admin = UserAdmin(User, admin.site)

  def test_get_exclude_superuser(self):

    """
    Teste qu'aucun champ n'est exclu de l'interface d'administration pour un superutilisateur.
    """

    # Simule une requête HTTP GET à l'interface d'administration
    request = self.factory.get('/')
    # Associe l'utilisateur superutilisateur à la requête
    request.user = self.superuser
    # Récupère la liste des champs à exclure de l'interface d'administration
    exclude = self.user_admin.get_exclude(request)

    self.assertEqual(exclude, [])
  
  def test_get_exclude_regular_user(self):
    
    """
    Teste que certains champs sont exclus de l'interface d'administration pour un administrateur en vérifiant que :
    - La liste attendue des champs exclus comprend : "groups", "password" et "user_permissions".
    """

    # Simule une requête HTTP GET à l'interface d'administration
    request = self.factory.get('/')
    # Associe l'utilisateur administrateur à la requête
    request.user = self.admin
    # Récupère la liste des champs à exclure de l'interface d'administration
    exclude = self.user_admin.get_exclude(request)

    self.assertEqual(exclude, ["groups", "password", "user_permissions"])