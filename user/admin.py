from django.conf import settings
from django.contrib import admin
from .models import Person, User

admin.site.site_header = "Administration de la billetterie des Jeux olympiques"
admin.site.site_url = settings.WEBSITE_URL

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
  
  list_display = ("lastname", "firstname", "date_of_birth", "country")
  list_filter = ("country",)
  ordering = ("lastname", "firstname")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  
  fieldsets = (
    (None, {
      "fields": ("email", "account_key")
    }),
    ("Informations personnelles", {
      "fields": ("firstname", "lastname", "date_of_birth", "country")
    }),
    ("Permissions", {
      "fields": ("is_active", "is_staff", "is_superuser", "user_permissions")
    }),
    ("Informations de connexion", {
      "fields": ("date_joined", "last_login")
    })
  )
  list_display = ("lastname", "firstname", "email", "account_key")
  ordering = ("lastname", "firstname")
  readonly_fields = ("account_key", "date_joined")

  @admin.display(description="Clé de compte")
  def account_key(self, obj: User) -> str:
    
    """
    Retourne la clé du compte de l'utilisateur.
    Args:
      obj (User): L'instance de l'utilisateur dont on veut obtenir la clé du compte.
    Returns:
      str: La clé du compte de l'utilisateur.
    """
    return obj.id_person