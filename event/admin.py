from django.contrib import admin
from django.utils.html import format_html
from .models import Competition, Event, Sport, Location

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):

  list_display = ('title', 'image_thumbnail')
  ordering = ('title',)

  def image_thumbnail(self, obj):

    """
    Génère une vignette d'image cliquable, qui s'ouvre dans une nouvelle fenêtre.
    Args:
      obj: Un objet qui doit avoir un attribut `image` avec une URL et un attribut `title` pour le texte alternatif de
        l'image.
    Returns:
      str: Une chaîne HTML contenant une balise `<a>` avec une image à l'intérieur si l'attribut `image` existe, sinon
        une chaîne vide.
    """
    if obj.image:

      return format_html(
        f'''<a href="{obj.image.url}" onclick="window.open(this.href, '_blank', 'withdowName=popup'); return false;">'''
          f'''<img src="{obj.image.url}" alt="{obj.title}" width="80"/>'''
        f'''</a>'''
      )
      
    return ''
  
  image_thumbnail.short_description = 'Vignette'




@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):

  list_display = ('name', 'city', 'total_seats')
  list_filter = ('city',)
  ordering = ('name',)




class EventInline(admin.TabularInline):

  model = Competition
  extra = 0


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

  inlines = [EventInline]
  list_display = ('sport', 'date', 'start_time', 'end_time', 'location_name', 'available_places')
  list_filter = ('sport', 'location__name')
  ordering = ('date', 'start_time', 'sport')

  def available_places(self, obj) -> str:

    """
    Retourne le nombre de places disponibles pour un événement donné, avec une couleur indiquant si le nombre est inférieur à 5 %.
    Args:
      obj: Un objet qui doit avoir un attribut `available_seats` et `location` avec un attribut `total_seats`.
    Returns:
      str: Une chaîne contenant le nombre de places disponibles, colorée en rouge si ce dernier est inférieur à 5 % du nombre total de places, sinon
        en vert.
    """
    threshold = obj.location.total_seats * 0.05
    color = 'red' if obj.available_seats < threshold else '#32CD32'

    return format_html(
      f'<span style="color: {color}; font-weight: bold;">{obj.available_seats}</span>'
    )
  
  def location_name(self, obj: Event) -> str:

    """
    Retourne le nom du lieu associé à l'événement.
    Args:
      obj (Event): L'instance de l'événement dont on veut obtenir le nom du lieu.
    Returns:
      str: Le nom du lieu associé à l'événement.
    """
    return obj.location.name
  
  available_places.short_description = 'Places disponibles'
  location_name.short_description = 'Lieu'




@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):

  list_display = ('description', 'gender', 'phase', 'event')
  list_filter = ('gender', 'event__sport')
  ordering = ('event__date', 'event__start_time', 'id_competition', 'event__sport')