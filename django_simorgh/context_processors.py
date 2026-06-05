from django.conf import settings
from django.templatetags.static import static


VALID_THEME_COLORS = {
    "green",
    "blue",
    "red",
    "yellow",
    "black",
    "purple",
    "orange",
    "pink",
    "navy",
}


def simorgh_context(request):
    color = getattr(settings, "DJANGO_ADMIN_THEME_COLOR", "green")
    if color not in VALID_THEME_COLORS:
        color = "green"

    return {
        "simorgh_site_header": getattr(settings, "DJANGO_ADMIN_SITE_HEADER", "Simorgh Admin"),
        "simorgh_theme_color": color,
        "simorgh_logo": getattr(
            settings,
            "DJANGO_ADMIN_LOGO",
            static("django_simorgh/img/logo.png"),
        ),
        "simorgh_favicon": getattr(
            settings,
            "DJANGO_ADMIN_FAVICON",
            static("django_simorgh/img/favicon.ico"),
        ),
    }
