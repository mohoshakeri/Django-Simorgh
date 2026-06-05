from django.apps import AppConfig


class DjangoSimorghConfig(AppConfig):
    name = "django_simorgh"
    verbose_name = "Django Simorgh"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        pass
