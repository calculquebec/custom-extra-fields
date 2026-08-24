"""
Admin configuration for custom_extra_fields models.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from custom_extra_fields.models import CustomExtraFields


@admin.register(CustomExtraFields)
class CustomExtraFieldsAdmin(admin.ModelAdmin):
    """
    Admin configuration for CustomExtraFields.
    """

    list_display = (
        "id",
        "user_username",
        "position",
        "wants_newsletter",
        "favorite_language",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    fieldsets = (
        (_("User Information"), {"fields": ("user", "position")}),
        (_("Preferences"), {"fields": ("favorite_language", "wants_newsletter")}),
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
