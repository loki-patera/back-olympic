import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import BookingLine

@receiver(post_delete, sender=BookingLine)
def delete_qr_code_image_on_bookingline_delete(instance, **kwargs) -> None:
    
  """
  Supprime le fichier image du QR code associé à la ligne de réservation lors de sa suppression.
  """
  # Vérifie si l'instance a un champ `qr_code_image` et si le chemin du fichier existe
  if instance.qr_code_image and instance.qr_code_image.path:
    
  # Vérifie si le fichier d'image du QR code existe
    if os.path.isfile(instance.qr_code_image.path):
      
      # Supprime le fichier d'image du QR code
      os.remove(instance.qr_code_image.path)