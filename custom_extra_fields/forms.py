"""
Forms for custom extra fields.
"""

from django import forms
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from custom_extra_fields.conf import get_sla_url, get_sla_version
from custom_extra_fields.models import CustomExtraFields


class SlaAcceptanceWidget(forms.CheckboxInput):
    """
    Checkbox widget that renders a clickable link to the SLA document.

    The label includes the SLA version and a hyperlink to the document URL,
    both sourced dynamically from ``custom_extra_fields.conf`` so they
    automatically reflect the current settings values.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        sla_url = get_sla_url()
        sla_version = get_sla_version()
        checkbox_html = super().render(name, value, attrs, renderer)

        if sla_url:
            link = f'<a href="{sla_url}" target="_blank" rel="noopener noreferrer">v{sla_version}</a>'
        else:
            link = f"v{sla_version}"

        label = _(
            "I have read and accept the Service Level Agreement (SLA) {link}."
        ).format(link=link)
        return mark_safe(f"{checkbox_html} {label}")


class SlaAcceptanceField(forms.BooleanField):
    """
    A required BooleanField that enforces SLA acceptance.

    Uses :class:`SlaAcceptanceWidget` to display a link to the SLA document
    inline with the checkbox.
    """

    widget = SlaAcceptanceWidget

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", True)
        kwargs.setdefault(
            "error_messages",
            {"required": _("You must accept the SLA to complete your registration.")},
        )
        super().__init__(*args, **kwargs)


class CustomExtraFieldsForm(ModelForm):
    """
    Form that represents user extra info and is compatible with edX's FormDescription system.

    Adding a field as 'required' will make it mandatory for the user to fill it in, and
    and will show it in the registration form.
    """

    sla_acceptance = SlaAcceptanceField(
        label=_("SLA acceptance"),
        help_text=_("You must accept the Service Level Agreement to register."),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Check box field
        self.fields["wants_newsletter"].help_text = "Abonnez-vous à notre infolettre pour recevoir les dernières informations sur le contenu d'evolo"
        self.fields["wants_newsletter"].label = "M'abonner à l'infolettre"

        # Select fields
        self.fields["position"].help_text = "Choisissez votre statut académique"
        self.fields["position"].label = "Statut académique"
        self.fields["research_area"].help_text = "Choisissez votre domaine de recherche."
        self.fields["research_area"].label = "Domaine de recherche"

    class Meta:
        model = CustomExtraFields
        fields = [
            "position",
            "research_area",
            "wants_newsletter",
        ]
