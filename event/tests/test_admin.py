from django.test import TestCase
from unittest.mock import Mock
from event.admin import EventAdmin, SportAdmin

class SportAdminTests(TestCase):

  def setUp(self):

    """
    Crée une instance de `SportAdmin` avec des objets Mock pour le modèle et le site admin
    """
    self.admin = SportAdmin(model=Mock(), admin_site=Mock())


  def test_image_thumbnail_with_image(self):

    """
    Teste la méthode `image_thumbnail` lorsque l'objet a une image
    """
    # Création d'un objet Mock avec des attributs `image` et `title`
    obj = Mock()
    obj.image.url = "http://example.com/surf.jpg"
    obj.title = "surf"

    # Appel de la méthode `image_thumbnail`
    result = self.admin.image_thumbnail(obj)

    # HTML attendu en sortie
    expected_html = (
      f'''<a href="http://example.com/surf.jpg" onclick="window.open(this.href, '_blank', 'withdowName=popup'); return false;">'''
        f'''<img src="http://example.com/surf.jpg" alt="surf" width="80"/>'''
      f'''</a>'''
    )

    self.assertEqual(result, expected_html)


  def test_image_thumbnail_without_image(self):

    """
    Teste la méthode `image_thumbnail` lorsque l'objet n'a pas d'image
    """
    # Création d'un objet Mock sans attribut `image`
    obj = Mock()
    obj.image = None

    # Appel de la méthode `image_thumbnail`
    result = self.admin.image_thumbnail(obj)

    self.assertEqual(result, '')




class EventAdminTests(TestCase):

  def setUp(self):

    """
    Crée une instance de `EventAdmin` avec des objets Mock pour le modèle et le site admin
    """
    self.admin = EventAdmin(model=Mock(), admin_site=Mock())
  
  def test_available_places_above_threshold(self):

    """
    Teste que le nombre de places disponibles est affiché en vert si >= 5% du total.
    """
    # Création d'un objet Mock avec des attributs `total_seats` et `available_seats`
    obj = Mock()
    obj.location.total_seats = 100
    obj.available_seats = 10

    # Appel de la méthode `available_places`
    result = self.admin.available_places(obj)

    # Style HTML attendu en sortie
    expected_html = '<span style="color: #32CD32; font-weight: bold;">10</span>'
    self.assertEqual(result, expected_html)

  def test_available_places_below_threshold(self):

    """
    Teste que le nombre de places disponibles est affiché en rouge si < 5% du total.
    """
    # Création d'un objet Mock avec des attributs `total_seats` et `available_seats`
    obj = Mock()
    obj.location.total_seats = 200
    obj.available_seats = 9

    # Appel de la méthode `available_places`
    result = self.admin.available_places(obj)

    # Style HTML attendu en sortie
    expected_html = '<span style="color: red; font-weight: bold;">9</span>'
    self.assertEqual(result, expected_html)

  def test_available_places_exactly_at_threshold(self):

    """
    Teste que le nombre de places disponibles est affiché en vert si exactement 5% du total.
    """
    # Création d'un objet Mock avec des attributs `total_seats` et `available_seats`
    obj = Mock()
    obj.location.total_seats = 40
    obj.available_seats = 2

    # Appel de la méthode `available_places`
    result = self.admin.available_places(obj)

    # Style HTML attendu en sortie
    expected_html = '<span style="color: #32CD32; font-weight: bold;">2</span>'
    self.assertEqual(result, expected_html)
  
  def test_location_name_returns_location_name(self):

    """
    Teste que la méthode `location_name` retourne le nom du lieu associé à l'événement.
    """
    # Création d'un objet Mock avec un attribut `location` ayant un attribut `name`
    obj = Mock()
    obj.location.name = "Arena Paris Sud 6"
    
    # Appel de la méthode `location_name`
    result = self.admin.location_name(obj)
    
    self.assertEqual(result, "Arena Paris Sud 6")