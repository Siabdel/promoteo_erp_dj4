from django.apps import AppConfig
from django.dispatch import Signal

class CalendarConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "calendar"

    def ready(self):
        import core.calendar.signals  # noqa F401