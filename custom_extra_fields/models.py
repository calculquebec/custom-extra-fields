"""
Database models for custom_extra_fields.
"""

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomExtraFields(models.Model):
    """
    Model that extends the User model with custom fields.
    """

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    position = models.CharField(
        blank=True,
        max_length=50,
        choices=[
            ("undergraduate_student", _("Étudiant-e au premier cycle")),
            ("masters_student", _("Étudiant-e à la maîtrise")),
            ("doctoral_student", _("Étudiant-e au doctorat")),
            ("postdoctoral_fellow", _("Stagiaire post-doctoral")),
            ("professor", _("Professeur-e")),
            ("research_professional", _("Professionnel-le de recherche")),
            ("other", _("Autre")),
        ],
        verbose_name=_("Position"),
    )

    wants_newsletter = models.BooleanField(
        default=False,
        verbose_name=_("Subscribe to newsletter"),
    )

    favorite_language = models.CharField(
        blank=True,
        max_length=50,
        choices=[
            ("python", "Python"),
            ("javascript", "JavaScript"),
            ("java", "Java"),
            ("go", "Go"),
        ],
        verbose_name=_("Favorite programming language"),
    )

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        return f"<CustomExtraFields, ID: {self.id}>"
