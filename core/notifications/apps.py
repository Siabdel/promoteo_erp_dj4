from django.apps import AppConfig

class NotificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'  # Simplifiez le nom si nécessaire
    
    def ready(self):
        import core.notifications.signals  # noqa F401