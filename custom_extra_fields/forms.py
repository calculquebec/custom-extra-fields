"""
Forms for custom extra fields.
"""

from django.forms import ModelForm

from custom_extra_fields.models import CustomExtraFields


class CustomExtraFieldsForm(ModelForm):
    """
    Form that represents user extra info and is compatible with edX's FormDescription system.

    Adding a field as 'required' will make it mandatory for the user to fill it in, and
    and will show it in the registration form.
    """

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
