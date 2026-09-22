# Generated migration for UserSlaAcceptance model

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("custom_extra_fields", "0003_remove_customextrafields_birthdate_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserSlaAcceptance",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "accepted_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="Accepted at",
                    ),
                ),
                (
                    "sla_version",
                    models.CharField(
                        help_text="Version of the SLA that was accepted (copied from settings at acceptance time).",
                        max_length=50,
                        verbose_name="SLA version",
                    ),
                ),
                (
                    "sla_url",
                    models.URLField(
                        help_text="URL of the SLA document that was accepted (copied from settings at acceptance time).",
                        max_length=500,
                        verbose_name="SLA URL",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sla_acceptance",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "User SLA acceptance",
                "verbose_name_plural": "User SLA acceptances",
                "db_table": "custom_extra_fields_user_sla_acceptance",
            },
        ),
    ]
