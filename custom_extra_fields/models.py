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

    research_area = models.CharField(
        blank=True,
        max_length=50,
        choices=[
            ("natural_sciences", _("Sciences naturelles")),
            ("engineering_and_technology", _("Génie et technologies")),
            ("medical_health_and_life_sciences", _("Sciences médicales, de la santé et de la vie")),
            ("agricultural_and_veterinary_sciences", _("Sciences agricoles et vétérinaires")),
            ("social_sciences", _("Sciences sociales")),
            ("humanities_and_the_arts", _("Sciences humaines et arts")),
        ],
        verbose_name=_("Research area"),
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
