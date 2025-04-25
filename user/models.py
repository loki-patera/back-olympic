import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models

class AccountUserManager(UserManager):

  def _create_user(self, email: str, password: str = None, **extra_fields):

    """
    Crée et enregistre un utilisateur avec un email valide et un mot de passe sécurisé.
    Args:
      email (str): L'adresse email de l'utilisateur. Doit être une adresse email valide.
      password (str): Le mot de passe pour l'utilisateur.
      **extra_fields: Champs supplémentaires à inclure lors de la création de l'utilisateur.
    Raises:
      ValueError: Si l'email n'est pas fourni.
    Returns:
      user: L'instance de l'utilisateur créé.
    """

    if not email:
      raise ValueError("Vous n'avez pas donné une adresse email valide")
    
    email = self.normalize_email(email)

    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)

    return user
  
  def create_user(self, email: str|None = None, password: str|None = None, **extra_fields):

    """
    Crée et retourne un nouvel utilisateur qui n'est pas membre du staff et superutilisateur.
    Args:
      email (str, optional): L'adresse email de l'utilisateur. Par défaut None.
      password (str, optional): Le mot de passe pour l'utilisateur. Par défaut None.
      **extra_fields: Champs supplémentaires défini pour un utilisateur.
    Returns:
      User: L'instance de l'utilisateur créée via _create_user.
    """

    extra_fields.setdefault('is_staff', False)
    extra_fields.setdefault('is_superuser', False)

    return self._create_user(email, password, **extra_fields)
  
  def create_superuser(self, email: str|None = None, password: str|None = None, **extra_fields):

    """
    Crée et retourne un superutilisateur.
    Args:
      email (str, optional): L'adresse email du superutilisateur. Par défaut None.
      password (str, optional): Le mot de passe pour le superutilisateur. Par défaut None.
      **extra_fields: Champs supplémentaires défini pour un superutilisateur.
    Returns:
      User: L'instance du superutilisateur créée via _create_user.
    """

    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)

    return self._create_user(email, password, **extra_fields)


class Person(models.Model):

  id_person = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  firstname = models.CharField(max_length=50, null=False, verbose_name="Prénom")
  lastname = models.CharField(max_length=50, null=False, verbose_name="Nom de famille")
  date_of_birth = models.DateField(null=False, verbose_name="Date de naissance")
  country = models.CharField(max_length=75, null=False, verbose_name="Pays")

  class Meta:

    verbose_name = "Personne"
    verbose_name_plural = "Personnes"
  
  def __str__(self) -> str:

    """
    Retourne une représentation sous forme de chaîne du nom complet.
    Returns:
      str: Une chaîne au format "prénom nom de famille".
    """

    return f"{self.firstname} {self.lastname}"


class User(Person, AbstractBaseUser, PermissionsMixin):

  email = models.EmailField(max_length=100, unique=True, null=False, verbose_name="Email")

  is_active = models.BooleanField(default=True, verbose_name="Actif")
  is_staff = models.BooleanField(default=False, verbose_name="Membre du staff")
  is_superuser = models.BooleanField(default=False, verbose_name="Super utilisateur")

  date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
  last_login = models.DateTimeField(blank=True, null=True, verbose_name="Dernière connexion")

  objects = AccountUserManager()

  USERNAME_FIELD = 'email'
  EMAIL_FIELD = 'email'
  REQUIRED_FIELDS = ['firstname', 'lastname', 'date_of_birth', 'country']

  class Meta:

    verbose_name = "Client"
    verbose_name_plural = "Clients"