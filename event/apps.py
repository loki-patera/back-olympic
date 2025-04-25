from django.apps import AppConfig

class EventConfig(AppConfig):
    
  default_auto_field = "django.db.models.BigAutoField"
  name = "event"
  verbose_name = "Gestion des événements sportifs"

  def ready(self):

    """
    Importe les gestionnaires de signaux pour l'application.
    """
    import event.signals