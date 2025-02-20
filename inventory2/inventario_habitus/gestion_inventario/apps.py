from django.apps import AppConfig

class GestionInventarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion_inventario'

    def ready(self):
        import gestion_inventario.signals
