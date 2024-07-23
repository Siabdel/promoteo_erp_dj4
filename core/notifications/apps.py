from django.apps import AppConfig
from django.dispatch import Signal

class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notification"

    def ready(self):
        import notification.signals  # noqa F401