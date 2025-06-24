from django.apps import AppConfig

class BookingConfig(AppConfig):

  default_auto_field = "django.db.models.BigAutoField"
  name = "booking"
  verbose_name = "Gestion des réservations"

  def ready(self):
    
    """
    Importe les gestionnaires de signaux pour l'application.
    """
    import booking.signals