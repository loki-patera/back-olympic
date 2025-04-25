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