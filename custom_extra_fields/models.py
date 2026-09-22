"""
Database models for custom_extra_fields.
"""

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserSlaAcceptance(models.Model):
    """
    Records that a user has accepted a specific version of the SLA.

    The ``sla_version`` and ``sla_url`` fields capture the values that were
    active in settings at the moment of acceptance, so the audit trail remains
    accurate even when settings change later.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="sla_acceptance",
        verbose_name=_("User"),
    )
    accepted_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Accepted at"),
    )
    sla_version = models.CharField(
        max_length=50,
        verbose_name=_("SLA version"),
        help_text=_("Version of the SLA that was accepted (copied from settings at acceptance time)."),
    )
    sla_url = models.URLField(
        max_length=500,
        verbose_name=_("SLA URL"),
        help_text=_("URL of the SLA document that was accepted (copied from settings at acceptance time)."),
    )

    class Meta:
        db_table = "custom_extra_fields_user_sla_acceptance"
        verbose_name = _("User SLA acceptance")
        verbose_name_plural = _("User SLA acceptances")

    def __str__(self):
        return f"{self.user.username} accepted SLA v{self.sla_version} on {self.accepted_at}"


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

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        return f"<CustomExtraFields, ID: {self.id}>"
