"""
Configuration helpers for custom_extra_fields.

All SLA-related settings are read from Django settings with sensible defaults.
To configure them in your project's settings file::

    CUSTOM_EXTRA_FIELDS_SLA_URL = "https://example.com/sla"
    CUSTOM_EXTRA_FIELDS_SLA_VERSION = "1.0"

Both settings are required for the SLA acceptance feature to work at
registration time.  The values are copied into the database record at the
moment of acceptance so that the audit trail remains accurate even when the
settings change later.
"""

from django.conf import settings


def get_sla_url():
    """Return the URL of the current SLA document from Django settings."""
    return getattr(settings, "CUSTOM_EXTRA_FIELDS_SLA_URL", "")


def get_sla_version():
    """Return the version string of the current SLA from Django settings."""
    return getattr(settings, "CUSTOM_EXTRA_FIELDS_SLA_VERSION", "")
