"""
URLs for custom_extra_fields.
"""

from django.urls import path

from custom_extra_fields.views import sla_accept_view

urlpatterns = [
    path("sla/accept/", sla_accept_view, name="sla_accept"),
]
