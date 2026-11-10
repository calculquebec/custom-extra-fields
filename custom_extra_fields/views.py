import json
from urllib.parse import quote

from django import forms
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

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


@csrf_exempt
@login_required
def sla_accept_view(request):
    """
    GET  — Redirect to the frontend SLA page (get_sla_url()) with ?next=...,
           or render the fallback HTML template if no SLA URL is configured.
    POST — Validate acceptance (from JSON payload or form-encoded POST),
           persist UserSlaAcceptance, and return JSON or redirect to ``next``.
    """
    next_url = request.GET.get("next") or request.POST.get("next") or "/"
    sla_url = get_sla_url()
    sla_version = get_sla_version()

    # Respect language preference cookie (e.g. 'fr' or 'fr-ca')
    lang_pref = request.COOKIES.get("openedx-language-preference", "")
    if lang_pref.lower().startswith("fr"):
        translation.activate("fr")

    if request.method == "POST":
        accepted = False
        is_json = (
            request.content_type == "application/json"
            or "application/json" in request.headers.get("accept", "")
        )

        if request.content_type == "application/json":
            try:
                body_data = json.loads(request.body.decode("utf-8"))
            except Exception:  # pylint: disable=broad-except
                body_data = {}
            accepted = bool(body_data.get("accepted"))
            next_url = body_data.get("next") or next_url
        else:
            form = SlaAcceptanceForm(request.POST)
            if form.is_valid():
                accepted = True
            next_url = request.POST.get("next") or next_url

        if accepted:
            UserSlaAcceptance.objects.update_or_create(
                user=request.user,
                defaults={
                    "sla_version": sla_version,
                    "sla_url": sla_url,
                },
            )
            if is_json:
                return JsonResponse({"success": True, "redirect_url": next_url})
            return redirect(next_url)

        if is_json:
            return JsonResponse({"success": False, "error": "SLA acceptance is required."}, status=400)

    # GET request with JSON Accept header (status query from MFE)
    is_json = (
        request.content_type == "application/json"
        or "application/json" in request.headers.get("accept", "")
    )
    if is_json:
        has_accepted = False
        if request.user.is_authenticated and sla_version:
            try:
                has_accepted = (request.user.sla_acceptance.sla_version == sla_version)
            except Exception:  # pylint: disable=broad-except
                has_accepted = False
        return JsonResponse({
            "is_authenticated": request.user.is_authenticated,
            "has_accepted": has_accepted,
            "sla_version": sla_version,
            "sla_url": sla_url,
        })

    # GET request: if an SLA page URL is configured (e.g. MFE static-pages), redirect to it
    if sla_url and not request.path.startswith(sla_url):
        separator = "&" if "?" in sla_url else "?"
        return redirect(f"{sla_url}{separator}next={quote(next_url)}")

    form = SlaAcceptanceForm()
    return render(
        request,
        "custom_extra_fields/sla_accept.html",
        {
            "form": form,
            "sla_url": sla_url,
            "sla_version": sla_version,
            "next": next_url,
            "is_french": lang_pref.lower().startswith("fr"),
        },
    )
