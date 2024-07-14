from django.apps import AppConfig


class Csc1106AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'csc1106app'

    def ready(self):
        import csc1106app.signals