from django import template
from django.apps import apps
from django.conf import settings
from django.contrib import admin

register = template.Library()

DEFAULT_APP_ICONS = {
    "auth": "fa-solid fa-shield-halved",
    "admin": "fa-solid fa-clock-rotate-left",
    "contenttypes": "fa-solid fa-layer-group",
    "sessions": "fa-solid fa-key",
    "sites": "fa-solid fa-globe",
}

DEFAULT_MODEL_ICONS = {
    "User": "fa-solid fa-user",
    "Group": "fa-solid fa-users",
    "LogEntry": "fa-solid fa-clock-rotate-left",
    "Permission": "fa-solid fa-user-lock",
    "ContentType": "fa-solid fa-layer-group",
    "Session": "fa-solid fa-key",
    "Site": "fa-solid fa-globe",
}


def _settings_icons():
    icons = getattr(settings, "DJANGO_ADMIN_ICONS", {})
    return icons if isinstance(icons, dict) else {}


@register.filter
def simorgh_app_icon(app):
    app_label = app.get("app_label") if isinstance(app, dict) else str(app)
    configured = _settings_icons().get(app_label, {})
    if isinstance(configured, dict):
        icon = configured.get("_app_icon")
        if icon:
            return icon

    app_config = apps.app_configs.get(app_label)
    if app_config is not None:
        for model_class in app_config.get_models():
            icon = getattr(model_class._meta, "simorgh_app_icon", None)
            if icon:
                return icon

    return DEFAULT_APP_ICONS.get(app_label, "fa-solid fa-folder")


@register.filter
def simorgh_model_icon(model):
    if not isinstance(model, dict):
        return "fa-solid fa-circle-dot"

    app_label = model.get("app_label", "")
    object_name = model.get("object_name", "")

    try:
        model_class = apps.get_model(app_label, object_name, require_ready=False)
    except (LookupError, ValueError):
        model_class = None

    if model_class is not None:
        meta_icon = getattr(model_class._meta, "simorgh_icon", None)
        if meta_icon:
            return meta_icon

        model_admin = admin.site._registry.get(model_class)
        icon = getattr(model_admin, "icon", None)
        if icon:
            return icon

    configured = _settings_icons().get(app_label, {})
    if isinstance(configured, dict):
        icon = configured.get(object_name)
        if icon:
            return icon

    return DEFAULT_MODEL_ICONS.get(object_name, "fa-solid fa-circle-dot")


@register.filter
def simorgh_initials(user):
    name = user.get_full_name() or user.get_username() or "A"
    parts = [part[0] for part in name.split() if part]
    return "".join(parts[:2]).upper() or "A"
