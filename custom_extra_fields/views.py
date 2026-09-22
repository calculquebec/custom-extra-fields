"""
Views for custom_extra_fields.
"""

from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from custom_extra_fields.conf import get_sla_url, get_sla_version
from custom_extra_fields.models import UserSlaAcceptance


class SlaAcceptanceForm(forms.Form):
    """
    Simple form that requires the user to tick a checkbox to accept the SLA.
    """

    accepted = forms.BooleanField(
        required=True,
        label=_("I have read and accept the Service Level Agreement."),
        error_messages={
            "required": _("You must accept the SLA to continue."),
        },
    )


@login_required
def sla_accept_view(request):
    """
    GET  — display the SLA acceptance form with a link to the current document.
    POST — validate the form, persist the acceptance record, redirect to ``next``.

    The acceptance record is stored via ``update_or_create`` so that re-accepting
    a new version simply overwrites the previous one (latest version only).
    """
    next_url = request.GET.get("next") or request.POST.get("next") or "/"
    sla_url = get_sla_url()
    sla_version = get_sla_version()

    if request.method == "POST":
        form = SlaAcceptanceForm(request.POST)
        if form.is_valid():
            UserSlaAcceptance.objects.update_or_create(
                user=request.user,
                defaults={
                    "sla_version": sla_version,
                    "sla_url": sla_url,
                },
            )
            return redirect(next_url)
    else:
        form = SlaAcceptanceForm()

    return render(
        request,
        "custom_extra_fields/sla_accept.html",
        {
            "form": form,
            "sla_url": sla_url,
            "sla_version": sla_version,
            "next": next_url,
        },
    )
