from django.test import TestCase
from unittest.mock import Mock
from event.admin import SportAdmin

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
    # Création d'un objet Mock avec des attributs image et title
    obj = Mock()
    obj.image.url = "http://example.com/surf.jpg"
    obj.title = "surf"

    # Appel de la méthode `image_tag`
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
    # Création d'un objet Mock sans attribut image
    obj = Mock()
    obj.image = None

    # Appel de la méthode `image_tag`
    result = self.admin.image_thumbnail(obj)

    self.assertEqual(result, '')