import numpy as np
import qrcode
import uuid
from django.core.files.base import ContentFile
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from io import BytesIO
from PIL import Image
from event.models import Event
from offer.models import Offer
from user.models import Person

class Booking(models.Model):

  id_booking = models.UUIDField(
    default=uuid.uuid4,
    editable=False,
    primary_key=True
  )
  booking_date = models.DateTimeField(
    auto_now_add=True,
    null=False,
    verbose_name="Date de réservation"
  )
  person = models.ForeignKey(
    Person,
    null=False,
    on_delete=models.CASCADE,
    verbose_name="Personne"
  )

  class Meta:

    verbose_name = "Réservation"
    verbose_name_plural = "Réservations"
  
  def __str__(self) -> str:

    """
    Retourne une représentation sous forme de chaîne de la réservation.
    Returns:
      str : La représentation de la réservation.
    """
    return f"{self.person.firstname} {self.person.lastname} ({timezone.localtime(self.booking_date).strftime("%d/%m/%Y %H:%M:%S")})"




class BookingLine(models.Model):

  id_booking_line = models.UUIDField(
    default=uuid.uuid4,
    editable=False,
    primary_key=True
  )
  qr_code = models.CharField(
    editable=False,
    max_length=73,
    null=False,
    unique=True,
    validators=[
      RegexValidator(
        regex=r'^[0-9a-fA-F\-]{36}\|[0-9a-fA-F\-]{36}$',
        message="Le QR code doit être de la forme <UUID>|<UUID>."
      )
    ],
    verbose_name="QR Code"
  )
  qr_code_image = models.ImageField(
    editable=False,
    null=False,
    upload_to='qr_codes',
    verbose_name="Image du QR Code"
  )
  booking = models.ForeignKey(
    Booking,
    null=False,
    on_delete=models.CASCADE,
    verbose_name="Réservation"
  )
  event = models.ForeignKey(
    Event,
    null=False,
    on_delete=models.CASCADE,
    verbose_name="Événement"
  )
  offer = models.ForeignKey(
    Offer,
    null=False,
    on_delete=models.CASCADE,
    verbose_name="Offre"
  )

  class Meta:

    verbose_name = "Ligne de réservation"
    verbose_name_plural = "Lignes de réservation"
  
  @property
  def buy_key(self) -> str:

    """
    Retourne la clé d'achat de la ligne de réservation.
    Returns:
      str: La clé d'achat de la ligne de réservation.
    """
    return str(self.id_booking_line)
  
  buy_key.fget.short_description = "Clé d'achat"

  @property
  def qr_code_thumbnail(self) -> str:

    if self.qr_code_image:

      return format_html(
        f'''<a href="{self.qr_code_image.url}" onclick="window.open(this.href, '_blank', 'withdowName=popup'); return false;">'''
          f'''<img src="{self.qr_code_image.url}" alt="QR code" width="80"/>'''
        f'''</a>'''
      )
    return ''
  
  qr_code_thumbnail.fget.short_description = "QR Code (Vignette)"

  def save(self, *args, **kwargs) -> None:

    """
    Enregistre la ligne de réservation et génère un QR code unique avec son image pour cette ligne de réservation.

    Args:
      *args: Arguments positionnels.
      **kwargs: Arguments nommés.
    Returns:
      None
    """
    # Génération du QR code
    self.qr_code = f"{str(self.id_booking_line)}|{str(self.booking.person.id_person)}"

    # Génération de l'image du QR code
    qr = qrcode.QRCode(
      version=1,
      error_correction=qrcode.constants.ERROR_CORRECT_L,
      box_size=10,
      border=5
    )
    qr.add_data(self.qr_code)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')

    # Création du gradient pour l'image du QR code
    width, height = img.size
    start_color = np.array([0x4b, 0xb1, 0xd7, 255])  # #4bb1d7
    end_color = np.array([0xff, 0xbd, 0x59, 255])    # #ffbd59
    gradient = np.zeros((height, width, 4), dtype=np.uint8)
    for x in range(width):
        ratio = x / (width - 1)
        color = (1 - ratio) * start_color + ratio * end_color
        gradient[:, x, :] = color
    
    # Application du gradient à l'image du QR code
    qr_array = np.array(img)
    mask = (qr_array[:, :, 0:3] == [0, 0, 0]).all(axis=2)
    qr_array[mask] = gradient[mask]
    img_gradient = Image.fromarray(qr_array, "RGBA")

    # Conversion de l'image en format PNG et sauvegarde dans un buffer
    buffer = BytesIO()
    img_gradient.save(buffer, format='PNG')
    random_filename = f"{uuid.uuid4()}.png"
    self.qr_code_image.save(
      random_filename,
      ContentFile(buffer.getvalue()),
      save=False
    )
    
    # Enregistrement de la ligne de réservation
    super().save(*args, **kwargs)
  
  def __str__(self) -> str:

    """
    Retourne une représentation sous forme de chaîne de la ligne de réservation.
    Returns:
      str : La représentation de la ligne de réservation.
    """
    return f"{self.booking} - {self.event}"