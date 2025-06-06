import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Sport

@receiver(post_delete, sender=Sport)
def delete_image_on_object_delete(instance: Sport, **kwargs) -> None:

  """
  Supprime le fichier d'image associé à l'instance de `Sport` lorsque l'instance est supprimée.
  """
  # Vérifie si l'instance a un champ image et si le fichier existe
  if instance.image:

    # Vérifie si le chemin du fichier d'image existe
    if os.path.isfile(instance.image.path):

      # Supprime le fichier d'image
      os.remove(instance.image.path)