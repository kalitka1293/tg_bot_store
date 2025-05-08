from django.apps import AppConfig


class MiniAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mini_app'

    def ready(self):
        import mini_app.signals