from django.contrib import admin
from django.utils.html import format_html
from .models import Booking, BookingLine

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    
  list_display = ("booking_date", "person")
  ordering = ("booking_date",)
  readonly_fields = ("booking_date",)
  search_fields = ("person__firstname", "person__lastname")

@admin.register(BookingLine)
class BookingLineAdmin(admin.ModelAdmin):
    
  list_display = ("booking", "event", "buy_key", "qr_code_thumbnail")
  readonly_fields = ("buy_key", "qr_code", "qr_code_image", "qr_code_thumbnail")

  @admin.display(description="Clé d'achat")
  def buy_key(self, obj: BookingLine) -> str:
      
    """
    Retourne la clé d'achat de la ligne de réservation.
    Args:
      obj (BookingLine): L'instance de la ligne de réservation dont on veut obtenir la clé d'achat.
    Returns:
      str: La clé d'achat de la ligne de réservation.
    """
    return obj.id_booking_line
  
  @admin.display(description="QR Code (Vignette)")
  def qr_code_thumbnail(self, obj: BookingLine) -> str:

    """
    Génère une vignette cliquable pour le QR code associé à la ligne de réservation, qui s'ouvre dans une nouvelle fenêtre.
    Args:
      obj (BookingLine): L'instance de la ligne de réservation qui doit avoir un attribut `qr_code_image` avec une URL.
    Returns:
      str: Une chaîne HTML contenant une balise `<a>` avec une image à l'intérieur si l'attribut `qr_code_image` existe, sinon une chaîne vide.
    """
    if obj.qr_code_image:

      return format_html(
        f'''<a href="{obj.qr_code_image.url}" onclick="window.open(this.href, '_blank', 'withdowName=popup'); return false;">'''
          f'''<img src="{obj.qr_code_image.url}" alt="QR code" width="80"/>'''
        f'''</a>'''
      )
    return ''