"""
custom_extra_fields Django application initialization.
"""

from django.apps import AppConfig


class CustomExtraFieldsConfig(AppConfig):
    """
    Configuration for the custom_extra_fields Django application.
    """

    name = "custom_extra_fields"
    default_auto_field = "django.db.models.AutoField"
    plugin_app = {
        "url_config": {
            "lms.djangoapp": {
                "namespace": "custom_extra_fields",
                "regex": r"^sla/",
                "relative_path": "urls",
            },
        },
    }
