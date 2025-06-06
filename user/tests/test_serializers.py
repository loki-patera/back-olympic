from datetime import date
from django.test import TestCase
from user.serializers import RegisterUserSerializer
from user.models import User
from rest_framework import serializers

class RegisterUserSerializerTests(TestCase):

  def setUp(self):

    """
    Configure les données de test pour le sérialiseur d'enregistrement d'utilisateur.
    """
    self.serializer = RegisterUserSerializer()

  def test_valid_email(self):
      
    """
    Teste la validation d'une adresse email valide.
    """
    email = "test@example.com"
    result = self.serializer.validate_email(email)
    assert result == email

  def test_email_too_long(self):

    """
    Teste la validation d'une adresse email trop longue.
    """
    email = "a" * 101 + "@example.com"
    with self.assertRaises(serializers.ValidationError) as context:
      self.serializer.validate_email(email)
    self.assertIn("ne doit pas dépasser 100 caractères", str(context.exception))

  def test_invalid_email_format(self):

    """
    Teste la validation d'une adresse email avec un format invalide.
    """
    email = "invalid-email"
    with self.assertRaises(serializers.ValidationError) as context:
      self.serializer.validate_email(email)
    self.assertIn("doit contenir minimum un caractère avant le '@'", str(context.exception))

  def test_email_already_exists(self):

    """
    Teste la validation d'une adresse email déjà utilisée.
    """
    User.objects.create(
        email="exists@example.com",
        password="motdepasseValide123!",
        firstname="Jean",
        lastname="Dupont",
        date_of_birth="1990-01-01",
        country="France"
    )
    email = "exists@example.com"
    with self.assertRaises(serializers.ValidationError) as context:
      self.serializer.validate_email(email)
    self.assertIn("déjà utilisé", str(context.exception))
  

  def test_valid_password(self):

    """
    Teste la validation d'un mot de passe valide.
    """
    password = "MotdepasseValide123!"
    result = self.serializer.validate_password(password)
    assert result == password
  
  def test_password_too_short(self):

    """
    Teste la validation d'un mot de passe trop court.
    """
    password = "Short1!"
    with self.assertRaises(serializers.ValidationError) as context:
      self.serializer.validate_password(password)
    self.assertIn("au moins 16 caractères", str(context.exception))
  
  def test_password_too_long(self):

    """
    Teste la validation d'un mot de passe trop long.
    """
    password = "A" * 129 + "1a!"
    with self.assertRaises(serializers.ValidationError) as context:
      self.serializer.validate_password(password)
    self.assertIn("ne doit pas dépasser 128 caractères", str(context.exception))
  
  def test_password_forbidden_characters(self):

    """
    Teste la validation d'un mot de passe avec des caractères interdits.
    """
    password = "MotdepasseValide123<"
    with self.assertRaises(serializers.ValidationError) as context:
      self.serializer.validate_password(password)
    self.assertIn("caractères interdits", str(context.exception))
  
  def test_password_missing_complexity(self):

    """
    Teste la validation d'un mot de passe sans complexité suffisante.
    """
    password = "motdepasseenminuscule1234"
    with self.assertRaises(serializers.ValidationError) as context:
      self.serializer.validate_password(password)
    self.assertIn("au moins une lettre majuscule", str(context.exception))
  

  def test_valid_firstname(self):

    """
    Teste la validation d'un prénom valide.
    """
    firstname = "Jean"
    result = self.serializer.validate_firstname(firstname)
    assert result == firstname
  
  def test_firstname_too_short(self):

    """
    Teste la validation d'un prénom trop court.
    """
    firstname = "J"
    with self.assertRaises(serializers.ValidationError) as context:
      self.serializer.validate_firstname(firstname)
    self.assertIn("au moins 2 caractères", str(context.exception))
  
  def test_firstname_too_long(self):

    """
    Teste la validation d'un prénom trop long.
    """
    firstname = "J" * 51
    with self.assertRaises(serializers.ValidationError) as context:
      self.serializer.validate_firstname(firstname)
    self.assertIn("ne doit pas dépasser 50 caractères", str(context.exception))
  
  def test_firstname_invalid_format(self):

    """
    Teste la validation d'un prénom avec un format invalide (ne commençant pas par une majuscule).
    """
    firstname = "jean"
    with self.assertRaises(serializers.ValidationError) as context:
      self.serializer.validate_firstname(firstname)
    self.assertIn("doit commencer par une majuscule", str(context.exception))
  
  def test_firstname_with_hyphen(self):
      
    """
    Teste la validation d'un prénom composé avec un tiret.
    """
    firstname = "Jean-Pierre"
    result = self.serializer.validate_firstname(firstname)
    assert result == firstname

  
  def test_valid_lastname(self):

    """
    Teste la validation d'un nom de famille valide.
    """
    lastname = "Dupont"
    result = self.serializer.validate_lastname(lastname)
    assert result == lastname
  
  def test_lastname_too_short(self):

    """
    Teste la validation d'un nom de famille trop court.
    """
    lastname = "D"
    with self.assertRaises(serializers.ValidationError) as context:
      self.serializer.validate_lastname(lastname)
    self.assertIn("au moins 2 caractères", str(context.exception))
  
  def test_lastname_too_long(self):

    """
    Teste la validation d'un nom de famille trop long.
    """
    lastname = "D" * 51
    with self.assertRaises(serializers.ValidationError) as context:
      self.serializer.validate_lastname(lastname)
    self.assertIn("ne doit pas dépasser 50 caractères", str(context.exception))
  
  def test_lastname_invalid_format(self):

    """
    Teste la validation d'un nom de famille avec un format invalide (ne commençant pas par une majuscule).
    """
    lastname = "dupont"
    with self.assertRaises(serializers.ValidationError) as context:
      self.serializer.validate_lastname(lastname)
    self.assertIn("doit commencer par une majuscule", str(context.exception))
  
  def test_lastname_with_hyphen(self):

    """
    Teste la validation d'un nom de famille composé avec un tiret.
    """
    lastname = "Dupont-Durand"
    result = self.serializer.validate_lastname(lastname)
    assert result == lastname
  
  
  def test_valid_date_of_birth(self):
      
    """
    Teste la validation d'une date de naissance valide (plus de 18 ans).
    """
    dob = date.today().replace(year=date.today().year - 20)
    result = self.serializer.validate_date_of_birth(dob)
    assert result == dob
  
  def test_too_young_date_of_birth(self):
      
    """
    Teste la validation d'une date de naissance pour un utilisateur de moins de 18 ans.
    """
    dob = date.today().replace(year=date.today().year - 17)
    with self.assertRaises(serializers.ValidationError) as context:
      self.serializer.validate_date_of_birth(dob)
    self.assertIn("au moins 18 ans", str(context.exception))
  
  def test_too_old_date_of_birth(self):
      
    """
    Teste la validation d'une date de naissance trop ancienne.
    """
    dob = date(1899, 12, 31)
    with self.assertRaises(serializers.ValidationError) as context:
      self.serializer.validate_date_of_birth(dob)
    self.assertIn("Date de naissance trop ancienne", str(context.exception))
  

  def test_valid_country(self):
      
    """
    Teste la validation d'un pays valide.
    """
    country = "France"
    result = self.serializer.validate_country(country)
    assert result == country
  
  def test_country_too_long(self):
      
    """
    Teste la validation d'un pays trop long.
    """
    country = "A" * 76
    with self.assertRaises(serializers.ValidationError) as context:
      self.serializer.validate_country(country)
    self.assertIn("ne doit pas dépasser 75 caractères", str(context.exception))
  
  def test_country_not_in_list(self):
      
    """
    Teste la validation d'un pays qui n'est pas dans la liste.
    """
    country = "Atlantide"
    with self.assertRaises(serializers.ValidationError) as context:
      self.serializer.validate_country(country)
    self.assertIn("n'est pas valide", str(context.exception))
  

  def test_create_user_success(self):
      
    """
    Teste la création d'un utilisateur avec des données valides.
    """
    data = {
      "email": "nouveau@example.com",
      "password": "MotdepasseValide123!",
      "firstname": "Alice",
      "lastname": "Martin",
      "date_of_birth": "1990-05-10",
      "country": "France"
    }
    user = self.serializer.create(data)
    assert user.email == data["email"]
    assert user.firstname == data["firstname"]
    assert user.lastname == data["lastname"]
    assert str(user.date_of_birth) == data["date_of_birth"]
    assert user.country == data["country"]
    assert user.check_password(data["password"])