from django.core.validators import MinValueValidator
from django.db import models

class Offer(models.Model):

  id_offer = models.SmallAutoField(
    null=False,
    primary_key=True
  )
  type = models.CharField(
    max_length=50,
    null=False,
    unique=True,
    verbose_name="Type d'offre"
  )
  number_seats = models.PositiveSmallIntegerField(
    null=False,
    validators=[MinValueValidator(1)],
    verbose_name="Nombre de places"
  )
  discount = models.PositiveSmallIntegerField(
    null=False,
    validators=[MinValueValidator(0)],
    verbose_name="Réduction (%)"
  )

  class Meta:

    verbose_name = "Offre"
    verbose_name_plural = "Offres"
  
  def __str__(self) -> str:
    """
    Retourne une représentation sous forme de chaîne du type d'offre.
    Returns:
      str : Le type d'offre.
    """
    return self.type