"""
URLs for custom_extra_fields.
"""

from django.urls import path

from custom_extra_fields.views import sla_accept_view

urlpatterns = [
    # Mounted at /sla/ via plugin_app regex r"^sla/"
    path("accept/", sla_accept_view, name="sla_accept"),
    # Also support direct inclusion at root without prefix
    path("sla/accept/", sla_accept_view, name="sla_accept_root"),
]
