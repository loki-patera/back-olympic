from django.test import TestCase
from unittest.mock import patch, MagicMock
from event.signals import delete_image_on_object_delete

class TestDeleteImageOnObjectDeleteSignal(TestCase):

  def setUp(self):

    """
    Crée une instance de `Sport` avec une image et une sans image.
    """
    self.sport_instance_with_image = MagicMock(image=MagicMock(path="/path/to/image.jpg"))
    self.sport_instance_without_image = MagicMock(image=None)


  @patch("os.path.isfile", return_value=True)   # Simule que le fichier existe
  @patch("os.remove")                           # Simule la suppression du fichier
  def test_delete_image_on_object_delete(self, mock_remove, mock_isfile):

    """
    Teste la fonction `delete_image_on_object_delete` lorsque le fichier image existe.
    """
    # Appel de la fonction à tester
    delete_image_on_object_delete(self.sport_instance_with_image)

    # Vérifie que `os.path.isfile` a été appelé avec le bon chemin
    mock_isfile.assert_called_once_with("/path/to/image.jpg")
    # Vérifie que `os.remove` a été appelé pour supprimer le fichier
    mock_remove.assert_called_once_with("/path/to/image.jpg")


  @patch("os.path.isfile", return_value=False)  # Simule que le fichier n'existe pas
  @patch("os.remove")                           # Simule la suppression du fichier
  def test_delete_image_on_object_delete_file_does_not_exist(self, mock_remove, mock_isfile):

    """
    Teste la fonction `delete_image_on_object_delete` lorsque le fichier image n'existe pas.
    """
    # Appel de la fonction à tester
    delete_image_on_object_delete(self.sport_instance_with_image)

    # Vérifie que `os.path.isfile` a été appelé avec le bon chemin
    mock_isfile.assert_called_once_with("/path/to/image.jpg")
    # Vérifie que `os.remove` n'a pas été appelé car le fichier n'existe pas
    mock_remove.assert_not_called()


  @patch("os.remove")                           # Simule la suppression du fichier
  def test_delete_image_on_object_delete_no_image(self, mock_remove):

    """"
    Teste la fonction `delete_image_on_object_delete` lorsque l'objet n'a pas d'image.
    """
    # Appel de la fonction à tester
    delete_image_on_object_delete(self.sport_instance_without_image)
    
    # Vérifie que `os.remove` n'a pas été appelé car il n'y a pas d'image
    mock_remove.assert_not_called()