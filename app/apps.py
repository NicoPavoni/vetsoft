from django.apps import AppConfig


class AppConfig(AppConfig):
    """
    Clase de la configuracion de la aplicacion.
    Se define nombre de la app.
    
    """
    
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
