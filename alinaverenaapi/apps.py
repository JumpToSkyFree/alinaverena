from django.apps import AppConfig


class AlinaverenaapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'alinaverenaapi'

    def ready(self) -> None:
        import alinaverenaapi.signals
        return super().ready()