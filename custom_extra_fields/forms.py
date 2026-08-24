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
        self.fields["wants_newsletter"].help_text = "Subscribe to our newsletter to get the latest news and updates."
        self.fields["wants_newsletter"].label = "Subscribe to newsletter?"

        # Select fields
        self.fields["position"].help_text = "Select your position."
        self.fields["research_area"].help_text = "Select your research area."
        self.fields["favorite_language"].help_text = "Pick your preferred programming language."

    class Meta:
        model = CustomExtraFields
        fields = [
            "position",
            "research_area",
            "wants_newsletter",
            "favorite_language",
        ]
