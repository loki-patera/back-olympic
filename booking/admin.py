from django.contrib import admin
from .models import Booking, BookingLine

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
  
  list_display = ("booking_date", "person")
  ordering = ("booking_date",)
  readonly_fields = ("booking_date",)
  search_fields = ("person__firstname", "person__lastname")
  search_help_text = "Prénom et/ou Nom du client"

@admin.register(BookingLine)
class BookingLineAdmin(admin.ModelAdmin):
  
  list_display = ("booking", "event", "buy_key", "qr_code_thumbnail")
  ordering = ("booking__booking_date", "event__date", "event__start_time")
  readonly_fields = ("buy_key", "qr_code", "qr_code_image", "qr_code_thumbnail")
  search_fields = ("booking__person__firstname", "booking__person__lastname")
  search_help_text = "Prénom et/ou Nom du client"