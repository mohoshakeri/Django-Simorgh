from django.db.models import options

for _name in ("simorgh_icon", "simorgh_app_icon"):
    if _name not in options.DEFAULT_NAMES:
        options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, _name)

default_app_config = "django_simorgh.apps.DjangoSimorghConfig"

__version__ = "1.0.1"
