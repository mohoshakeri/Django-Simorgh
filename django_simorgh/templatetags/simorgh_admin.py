from django import template
from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.urls import NoReverseMatch, reverse

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


def _clean_path(value):
    return str(value or "").split("?", 1)[0].split("#", 1)[0]


def _paths_match(current_path, target_path, include_children=False):
    current_path = _clean_path(current_path)
    target_path = _clean_path(target_path)

    if not current_path or not target_path:
        return False

    if current_path == target_path:
        return True

    if include_children and target_path.endswith("/"):
        return current_path.startswith(target_path)

    return False


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


@register.filter
def simorgh_is_current_url(url, request_path):
    return _paths_match(request_path, url)


@register.filter
def simorgh_model_is_current(model, request_path):
    if not isinstance(model, dict):
        return False

    return _paths_match(request_path, model.get("admin_url"), include_children=True)


@register.filter
def simorgh_app_is_current(app, request_path):
    if not isinstance(app, dict):
        return False

    app_label = app.get("app_label")
    if app_label:
        try:
            if _paths_match(request_path, reverse("admin:app_list", kwargs={"app_label": app_label}), include_children=True):
                return True
        except NoReverseMatch:
            pass

    return any(simorgh_model_is_current(model, request_path) for model in app.get("models", []))
