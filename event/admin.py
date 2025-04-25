from django.contrib import admin
from django.utils.html import format_html
from .models import Sport

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