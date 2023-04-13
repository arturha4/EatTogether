from django.apps import AppConfig


class FridgesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fridges'

    def ready(self):
        from fridges import scheduler
        scheduler.start()

