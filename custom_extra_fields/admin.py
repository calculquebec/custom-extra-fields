"""
Admin configuration for custom_extra_fields models.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from custom_extra_fields.models import CustomExtraFields, UserSlaAcceptance


@admin.register(CustomExtraFields)
class CustomExtraFieldsAdmin(admin.ModelAdmin):
    """
    Admin configuration for CustomExtraFields.
    """

    list_display = (
        "id",
        "user_username",
        "position",
        "research_area",
        "wants_newsletter",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    fieldsets = (
        (_("User Information"), {"fields": ("user", "position", "research_area")}),
        (_("Preferences"), {"fields": ("wants_newsletter",)}),
    )

    def user_username(self, obj):
        """
        Display the username of the related user.
        """
        if obj.user:
            return obj.user.username
        return _("No user")

    user_username.short_description = _("Username")
    user_username.admin_order_field = "user__username"


@admin.register(UserSlaAcceptance)
class UserSlaAcceptanceAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserSlaAcceptance.

    This model is intentionally read-only in the admin to preserve the
    integrity of the acceptance audit trail.
    """

    list_display = (
        "id",
        "user_username",
        "sla_version",
        "accepted_at",
        "sla_url",
    )

    list_filter = ("sla_version",)

    search_fields = (
        "user__username",
        "user__email",
        "sla_version",
    )

    readonly_fields = (
        "user",
        "accepted_at",
        "sla_version",
        "sla_url",
    )

    fieldsets = (
        (_("Acceptance Record"), {
            "fields": ("user", "accepted_at", "sla_version", "sla_url"),
        }),
    )

    def has_add_permission(self, request):
        """Prevent manual creation of acceptance records via the admin."""
        return False

    def has_change_permission(self, request, obj=None):
        """Prevent editing of acceptance records to preserve the audit trail."""
        return False

    def user_username(self, obj):
        """Display the username of the related user."""
        return obj.user.username

    user_username.short_description = _("Username")
    user_username.admin_order_field = "user__username"
