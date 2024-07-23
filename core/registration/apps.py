from django.apps import AppConfig
from django.dispatch import Signal

class RegistrationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "registration"

    def ready(self):
        import registrations.signals  # noqa F401