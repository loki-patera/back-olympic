import re
from datetime import date
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token
from .models import User

COUNTRIES = [
    "Afghanistan", "Afrique du Sud", "Ahvenanmaa", "Albanie", "Algérie", "Allemagne", "Andorre", "Angola", "Anguilla", "Antarctique",
    "Antigua-et-Barbuda", "Arabie Saoudite", "Argentine", "Arménie", "Aruba", "Australie", "Autriche", "Azerbaïdjan", "Bahamas", "Bahreïn",
    "Bangladesh", "Barbade", "Belgique", "Belize", "Bénin", "Bermudes", "Bhoutan", "Biélorussie", "Birmanie", "Bolivie", "Bosnie-Herzégovine",
    "Botswana", "Brésil", "Brunei", "Bulgarie", "Burkina Faso", "Burundi", "Cambodge", "Cameroun", "Canada", "Chili", "Chine", "Chypre",
    "Cité du Vatican", "Colombie", "Comores", "Congo", "Congo (Rép. dém.)", "Corée du Nord", "Corée du Sud", "Costa Rica", "Côte d'Ivoire",
    "Croatie", "Cuba", "Curaçao", "Danemark", "Djibouti", "Dominique", "Égypte", "Émirats arabes unis", "Équateur", "Érythrée", "Espagne",
    "Estonie", "États-Unis", "Éthiopie", "Fidji", "Finlande", "France", "Gabon", "Gambie", "Géorgie", "Géorgie du Sud-et-les Îles Sandwich du Sud",
    "Ghana", "Gibraltar", "Grèce", "Grenade", "Groenland", "Guadeloupe", "Guam", "Guatemala", "Guernesey", "Guinée", "Guinée équatoriale",
    "Guinée-Bissau", "Guyana", "Guyane", "Haïti", "Honduras", "Hong Kong", "Hongrie", "Île Bouvet", "Île Christmas", "Île de Man", "Île Maurice",
    "Île Norfolk", "Îles Caïmans", "Îles Cocos", "Îles Cook", "Îles du Cap-Vert", "Îles Féroé", "Îles Heard-et-MacDonald", "Îles Malouines",
    "Îles Mariannes du Nord", "Îles Marshall", "Îles mineures éloignées des États-Unis", "Îles Pitcairn", "Îles Salomon", "Îles Turques-et-Caïques",
    "Îles Vierges britanniques", "Îles Vierges des États-Unis", "Inde", "Indonésie", "Irak", "Iran", "Irlande", "Islande", "Israël", "Italie",
    "Jamaïque", "Japon", "Jersey", "Jordanie", "Kazakhstan", "Kenya", "Kirghizistan", "Kiribati", "Kosovo", "Koweït", "Laos", "Lesotho", "Lettonie",
    "Liban", "Liberia", "Libye", "Liechtenstein", "Lituanie", "Luxembourg", "Macao", "Macédoine du Nord", "Madagascar", "Malaisie", "Malawi",
    "Maldives", "Mali", "Malte", "Maroc", "Martinique", "Mauritanie", "Mayotte", "Mexique", "Micronésie", "Moldavie", "Monaco", "Mongolie",
    "Monténégro", "Montserrat", "Mozambique", "Namibie", "Nauru", "Népal", "Nicaragua", "Niger", "Nigéria", "Niue", "Norvège", "Nouvelle-Calédonie",
    "Nouvelle-Zélande", "Oman", "Ouganda", "Ouzbékistan", "Pakistan", "Palaos (Palau)", "Palestine", "Panama", "Papouasie-Nouvelle-Guinée",
    "Paraguay", "Pays-Bas", "Pays-Bas caribéens", "Pérou", "Philippines", "Pologne", "Polynésie française", "Porto Rico", "Portugal", "Qatar",
    "République centrafricaine", "République dominicaine", "Réunion", "Roumanie", "Royaume-Uni", "Russie", "Rwanda", "Sahara Occidental",
    "Saint-Barthélemy", "Saint-Christophe-et-Niévès", "Saint-Marin", "Saint-Martin", "Saint-Pierre-et-Miquelon", "Saint-Vincent-et-les-Grenadines",
    "Sainte-Hélène, Ascension et Tristan da Cunha", "Sainte-Lucie", "Salvador", "Samoa", "Samoa américaines", "São Tomé et Príncipe", "Sénégal",
    "Serbie", "Seychelles", "Sierra Leone", "Singapour", "Slovaquie", "Slovénie", "Somalie", "Soudan", "Soudan du Sud", "Sri Lanka", "Suède",
    "Suisse", "Surinam", "Svalbard et Jan Mayen", "Swaziland", "Syrie", "Tadjikistan", "Taïwan", "Tanzanie", "Tchad", "Tchéquie",
    "Terres australes et antarctiques françaises", "Territoire britannique de l'océan Indien", "Thaïlande", "Timor oriental", "Togo", "Tokelau",
    "Tonga", "Trinité-et-Tobago", "Tunisie", "Turkménistan", "Turquie", "Tuvalu", "Ukraine", "Uruguay", "Vanuatu", "Venezuela", "Viêt Nam",
    "Wallis-et-Futuna", "Yémen", "Zambie", "Zimbabwe"
]

class RegisterUserSerializer(serializers.ModelSerializer):

  email = serializers.EmailField(min_length=6, max_length=100)
  password = serializers.CharField(write_only=True, min_length=16, max_length=128)
  firstname = serializers.CharField(min_length=2, max_length=50)
  lastname = serializers.CharField(min_length=2, max_length=50)
  date_of_birth = serializers.DateField()
  country = serializers.CharField(max_length=75)

  class Meta:

    model = User
    fields = (
      'email',
      'password',
      'firstname',
      'lastname',
      'date_of_birth',
      'country'
    )

  def validate_email(self, value: str) -> str:

    """
    Valide l'email fourni par l'utilisateur.

    Args:
      value (str): L'email à valider.
    Raises:
      serializers.ValidationError: Si l'email dépasse 100 caractères, n'est pas au format valide, ou est déjà utilisé.
    Returns:
      str: L'email validé.
    """
    if len(value) < 6:
      raise serializers.ValidationError("Email trop court !")

    if len(value) > 100:
      raise serializers.ValidationError("Email trop long !")
    
    if not re.match(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", value):
      raise serializers.ValidationError("Format de l'email invalide !")
    
    if User.objects.filter(email=value).exists():
      raise serializers.ValidationError("Cet email est déjà utilisé !")
    
    return value
  
  def validate_password(self, value: str) -> str:

    """
    Valide le mot de passe fourni par l'utilisateur.

    Args:
      value (str): Le mot de passe à valider.
    Raises:
      serializers.ValidationError: Si le mot de passe contient des caractères interdits, est trop court ou trop long, ou ne respecte pas les critères
        de complexité.
    Returns:
      str: Le mot de passe validé.
    """
    if re.search(r'[<>"\'`;\/\\|&()\[\]{}]', value):
      raise serializers.ValidationError("Caractères interdits dans le mot de passe !")
    
    if len(value) < 16:
      raise serializers.ValidationError("Mot de passe trop court !")
    
    if len(value) > 128:
      raise serializers.ValidationError("Mot de passe trop long !")
    
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d])[^\s]{16,128}$", value):
      raise serializers.ValidationError("Format du mot de passe invalide !")
    
    return value
  
  def validate_firstname(self, value: str) -> str:

    """
    Valide le prénom fourni par l'utilisateur.

    Args:
      value (str): Le prénom à valider.
    Raises:
      serializers.ValidationError: Si le prénom est trop court, trop long, ou ne respecte pas les critères de format.
    Returns:
      str: Le prénom validé.
    """
    if len(value) < 2:
      raise serializers.ValidationError("Prénom trop court !")
    
    if len(value) > 50:
      raise serializers.ValidationError("Prénom trop long !")
    
    if not re.match(r"^(?=.{2,50}$)[A-ZÀ-ÖÙ-Ý][a-zà-öù-ÿ]+(?:-[A-ZÀ-ÖÙ-Ý][a-zà-öù-ÿ]+)*$", value):
      raise serializers.ValidationError("Format du prénom invalide !")
    
    return value
  
  def validate_lastname(self, value: str) -> str:

    """
    Valide le nom de famille fourni par l'utilisateur.

    Args:
      value (str): Le nom de famille à valider.
    Raises:
      serializers.ValidationError: Si le nom de famille est trop court, trop long, ou ne respecte pas les critères de format.
    Returns:
      str: Le nom de famille validé.
    """
    if len(value) < 2:
      raise serializers.ValidationError("Nom de famille trop court !")
    
    if len(value) > 50:
      raise serializers.ValidationError("Nom de famille trop long !")
    
    if not re.match(r"^(?=.{2,50}$)[A-ZÀ-ÖÙ-Ý][a-zà-öù-ÿ]+(?:-[A-ZÀ-ÖÙ-Ý][a-zà-öù-ÿ]+)*$", value):
      raise serializers.ValidationError("Format du nom de famille invalide !")
    
    return value
  
  def validate_date_of_birth(self, value: date) -> date:

    """
    Valide la date de naissance fournie par l'utilisateur.

    Args:
      value (date): La date de naissance à valider.
    Raises:
      serializers.ValidationError: Si l'utilisateur a moins de 18 ans ou si la date est trop ancienne.
    Returns:
      date: La date de naissance validée.
    """
    today = date.today()
    min_birth = date(today.year - 18, today.month, today.day)

    if value > min_birth:
      raise serializers.ValidationError("Vous devez être majeur pour vous inscrire !")
    
    if value < date(1900, 1, 1):
      raise serializers.ValidationError("Date de naissance trop ancienne !")
        
    return value
  
  def validate_country(self, value: str) -> str:

    """
    Valide le pays fourni par l'utilisateur.

    Args:
      value (str): Le pays à valider.
    Raises:
      serializers.ValidationError: Si le pays est trop long ou n'est pas dans la liste des pays valides.
    Returns:
      str: Le pays validé.
    """
    if len(value) > 75:
      raise serializers.ValidationError("Pays trop long !")
    
    if value not in COUNTRIES:
      raise serializers.ValidationError("Pays invalide !")
    
    return value
  
  def create(self, validated_data: dict) -> User:

    """
    Crée un nouvel utilisateur avec les données validées.

    Args:
      validated_data (dict): Les données validées pour créer l'utilisateur.
    Returns:
      User: L'instance de l'utilisateur créé.
    """
    return User.objects.create_user(**validated_data)




class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

  @classmethod
  def get_token(cls, user: User) -> Token:

    """
    Obtient le token JWT pour l'utilisateur avec des informations supplémentaires.

    Args:
      user (User): L'utilisateur pour lequel le token est généré.
    Returns:
      Token: Le token JWT généré pour l'utilisateur.
    """
    return super().get_token(user)
  
  def validate(self, attrs: dict) -> dict:

    """
    Valide les données d'authentification et retourne le token JWT.

    Args:
      attrs (dict): Les données d'authentification fournies par l'utilisateur.
    Returns:
      dict: Le token JWT et les informations de l'utilisateur.
    """
    try:
      # Appel de la méthode parent pour valider les données
      data = super().validate(attrs)
    except (serializers.ValidationError, AuthenticationFailed):
      # Si une erreur de validation se produit, lève une exception avec un message d'erreur personnalisé
      raise serializers.ValidationError({"detail": "Mot de passe incorrect !"})
    
    return data




class UserLightSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = (
      'firstname',
      'lastname'
    )