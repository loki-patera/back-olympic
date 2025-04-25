from django.contrib import admin
from .models import Person, User

admin.site.site_header = "Administration de la billetterie des Jeux olympiques"

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
  
  list_display = ("lastname", "firstname", "date_of_birth", "country")
  list_filter = ("country",)
  ordering = ("lastname", "firstname")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  
  list_display = ("lastname", "firstname", "email")
  ordering = ("lastname", "firstname")

  def get_exclude(self, request, obj=None) -> (list | list[str]):

    """
    Détermine la liste des champs à exclure de l'interface d'administration selon les permissions de l'utilisateur.
    Args:
      request (HttpRequest): L'objet de requête HTTP contenant des informations sur l'utilisateur actuel et le contexte
        de la requête.
      obj (Model, optionnel): L'instance du modèle en cours d'édition. Par défaut, None.
    Returns:
      list: Une liste des noms de champs à exclure. Retourne une liste vide si l'utilisateur est un superutilisateur;
        sinon, exclut "groups", "password" et "user_permissions".
    """

    if request.user.is_superuser:
      return []
    
    return ["groups", "password", "user_permissions"]