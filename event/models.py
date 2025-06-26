from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum

class Sport(models.Model):

  id_sport = models.SmallAutoField(
    null=False,
    primary_key=True
  )
  title = models.CharField(
    max_length=30,
    null=False,
    unique=True,
    verbose_name='Sport'
  )
  image = models.ImageField(
    null=False,
    upload_to='sports',
    verbose_name='Image'
  )

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




class Location(models.Model):

  id_location = models.SmallAutoField(
    null=False,
    primary_key=True
  )
  name = models.CharField(
    max_length=50,
    null=False,
    unique=True,
    verbose_name="Lieu"
  )
  city = models.CharField(
    max_length=50,
    null=False,
    verbose_name="Ville"
  )
  total_seats = models.PositiveIntegerField(
    null=False,
    validators=[MaxValueValidator(80000)],
    verbose_name="Nombre total de places"
  )

  class Meta:

    verbose_name = "Lieu"
    verbose_name_plural = "Lieux"
  
  def __str__(self) -> str:

    """
    Retourne une représentation sous forme de chaîne du nom du lieu.
    Returns:
      str : Le nom du lieu.
    """
    return f'{self.name} ({self.city})'




class Event(models.Model):

  id_event = models.SmallAutoField(
    null=False,
    primary_key=True
  )
  sport = models.ForeignKey(
    Sport,
    null=False,
    on_delete=models.CASCADE,
    verbose_name="Épreuve sportive"
  )
  location = models.ForeignKey(
    Location,
    null=False,
    on_delete=models.CASCADE,
    verbose_name="Lieu"
  )
  date = models.DateField(
    null=False,
    verbose_name="Date"
  )
  start_time = models.TimeField(
    null=False,
    verbose_name="Heure de début"
  )
  end_time = models.TimeField(
    null=False,
    verbose_name="Heure de fin"
  )
  price = models.DecimalField(
    decimal_places=2,
    max_digits=5,
    null=False,
    validators=[MinValueValidator(0), MaxValueValidator(Decimal(999.99))],
    verbose_name="Prix (€)"
  )
  
  class Meta:

    verbose_name = "Événement"
    verbose_name_plural = "Événements"
  
  def __str__(self) -> str:

    """
    Retourne une représentation sous forme de chaîne de l'événement.
    Returns:
      str : Une chaîne décrivant l'événement, incluant le sport et la période.
    """
    return f'{self.sport} | {self.date.strftime("%d/%m/%Y")} ({self.start_time.strftime("%H:%M")} - {self.end_time.strftime("%H:%M")})'
     
  @property
  def available_seats(self) -> int:

    """
    Calcule le nombre de places disponibles pour l'événement.
    Returns:
      int : Le nombre de places disponibles, calculé en soustrayant le nombre de places réservées du nombre total de places.
    """
    from booking.models import BookingLine

    # Calcule le nombre de places réservées pour l'événement
    booked_seats = BookingLine.objects.filter(event=self).aggregate(
      total=Sum('offer__number_seats')
    )['total'] or 0
    
    return self.location.total_seats - booked_seats




class Competition(models.Model):

  class Gender(models.TextChoices):

    Femmes = "Femmes"
    Hommes = "Hommes"
    Mixte = "Mixte"

  id_competition = models.SmallAutoField(
    null=False,
    primary_key=True
  )
  description = models.CharField(
    max_length=50,
    null=False,
    verbose_name="Description"
  )
  gender = models.CharField(
    choices=Gender.choices,
    max_length=6,
    null=False,
    verbose_name="Genre"
  )
  phase = models.CharField(
    blank=True,
    max_length=50,
    null=True,
    verbose_name="Phase"
  )
  event = models.ForeignKey(
    Event,
    null=False,
    on_delete=models.CASCADE,
    verbose_name="Événement"
  )

  class Meta:
    
    verbose_name = "Compétition"
    verbose_name_plural = "Compétitions"
  
  def __str__(self) -> str:

    """
    Retourne une représentation sous forme de chaîne de la compétition.
    Returns:
      str : Une chaîne décrivant la compétition, incluant l'événement, la description, le genre et la phase.
    """
    return f'{self.event} | {self.description}, {self.gender}, {self.phase}'