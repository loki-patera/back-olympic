from django.conf import settings
from django.db import models

class Sport(models.Model):

  id_sport = models.SmallAutoField(primary_key=True, null=False)
  title = models.CharField(max_length=30, null=False, unique=True, verbose_name='Sport')
  image = models.ImageField(upload_to='sports', null=False, verbose_name='Image')

  class Meta:

    verbose_name = 'Épreuve sportive'
    verbose_name_plural = 'Épreuves sportives'
  
  def __str__(self) -> str:

    """
    Retourne une représentation sous forme de chaîne du nom de l'épreuve sportive.
    Returns:
      str : Le nom de l'épreuve sportive.
    """
    return self.title
  
  def image_url(self) -> str:

    """
    Retourne l'URL complète pour l'image associée au sport.
    Returns:
      str: L'URL complète de l'image, combinant l'URL de base du site web et l'URL relative de l'image.
    """
    return f'{settings.WEBSITE_URL}{self.image.url}'