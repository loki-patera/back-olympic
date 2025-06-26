import re
from rest_framework import serializers

class PaymentSerializer(serializers.Serializer):

  card_number = serializers.CharField(write_only=True)
  card_name = serializers.CharField(write_only=True)
  expiration_date = serializers.CharField(write_only=True)
  cvc = serializers.CharField(write_only=True)

  cart = serializers.ListField(child=serializers.DictField(), write_only=True)

  def validate_card_number(self, value: str) -> str:

    """
    Valide le numéro de carte de crédit.

    Args:
      value (str): Le numéro de carte de crédit à valider.
    Raises:
      serializers.ValidationError: Si le numéro de carte n'est pas valide.
    Returns:
      str: Le numéro de carte de crédit validé.
    """
    if not value:
      raise serializers.ValidationError("Le numéro de carte est requis.")
    
    sanitized = value.replace(" ", "")

    if not re.fullmatch(r"\d{16}", sanitized):
      raise serializers.ValidationError("Le numéro de carte doit contenir exactement 16 chiffres.")
    
    if re.fullmatch(r"(\d)\1{15}", sanitized):
      raise serializers.ValidationError("Le numéro de carte ne peut pas contenir que des chiffres identiques.")
    
    return sanitized
  
  def validate_card_name(self, value: str) -> str:

    """
    Valide le nom sur la carte de crédit.
    Args:
      value (str): Le nom à valider.
    Raises:
      serializers.ValidationError: Si le nom est invalide.
    Returns:
      str: Le nom validé.
    """
    if not value:
      raise serializers.ValidationError("Le nom sur la carte est requis.")

    if value.strip() != value:
      raise serializers.ValidationError("Le nom ne doit pas commencer ou finir par un espace.")

    parts = value.strip().split()
    if len(parts) < 2:
      raise serializers.ValidationError("Le nom doit comporter un prénom et un nom de famille, séparés par un espace.")

    for part in parts:
      if len(part) < 2:
        raise serializers.ValidationError("Chaque partie du nom doit contenir au moins 2 lettres.")

    # Regex pour valider chaque partie (prénom ou nom composé)
    word = r"[A-ZÀ-ÖÙ-ÝÇ][a-zà-öù-ÿç]+(?:-[A-ZÀ-ÖÙ-ÝÇ][a-zà-öù-ÿç]+)*"
    name_regex = re.compile(f"^{word}( {word})+$")
    if not name_regex.match(value.strip()):
      raise serializers.ValidationError("Le nom doit comporter un Prénom et un Nom de famille, séparés par un espace.")

    return value
  
  def validate_expiration_date(self, value: str) -> str:

    """
    Valide la date d'expiration de la carte de crédit.
    Args:
      value (str): La date d'expiration à valider.
    Raises:
      serializers.ValidationError: Si la date est invalide ou hors plage autorisée.
    Returns:
      str: La date d'expiration validée.
    """
    import datetime

    if not value:
      raise serializers.ValidationError("La date d'expiration est requise.")

    if not re.fullmatch(r"\d{4}-\d{2}", value):
      raise serializers.ValidationError("Le format de la date d'expiration incorrect.")

    try:
      year, month = map(int, value.split("-"))
      if not (1 <= month <= 12):
        raise ValueError
    except Exception:
      raise serializers.ValidationError("Date d'expiration invalide.")

    today = datetime.date.today()
    current_year, current_month = today.year, today.month

    # La date d'expiration doit être le mois courant ou plus tard
    if year < current_year or (year == current_year and month < current_month):
      raise serializers.ValidationError("La date d'expiration ne peut pas être passée.")

    # La date d'expiration ne doit pas être plus de 6 ans dans le futur
    max_year, max_month = current_year + 6, current_month
    if year > max_year or (year == max_year and month > max_month):
      raise serializers.ValidationError("La date d'expiration ne peut pas être plus de 6 ans dans le futur.")

    return value
  
  def validate_cvc(self, value: str) -> str:
      
    """
    Valide le code CVC de la carte de crédit.
    Args:
      value (str): Le code CVC à valider.
    Raises:
      serializers.ValidationError: Si le code CVC n'est pas valide.
    Returns:
      str: Le code CVC validé.
    """
    if not value:
      raise serializers.ValidationError("Le code CVC est requis.")

    sanitized = value.replace(" ", "")

    if not re.fullmatch(r"\d{3}", sanitized):
      raise serializers.ValidationError("Le code CVC doit comporter exactement 3 chiffres.")

    if re.fullmatch(r"(\d)\1{2}", sanitized):
      raise serializers.ValidationError("Le code CVC ne doit pas être composé de chiffres identiques.")

    return sanitized
  
  def validate_cart(self, value: list[dict]) -> list[dict]:
      
    """
    Valide le panier envoyé pour le paiement.
    Args:
      value (list[dict]): Liste des réservations à valider.
    Raises:
      serializers.ValidationError: Si le panier est vide ou mal formé.
    Returns:
      list[dict]: Le panier validé.
    """
    if not value or not isinstance(value, list):
      raise serializers.ValidationError("Le panier est vide.")

    for item in value:
      
      if "id_event" not in item or "id_offer" not in item:
        raise serializers.ValidationError("Chaque élément du panier doit contenir un événement et une offre.")

    return value