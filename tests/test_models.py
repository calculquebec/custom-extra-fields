#!/usr/bin/env python
"""
Tests for the `custom-extra-fields` models module.
"""

import pytest
from django.contrib.auth import get_user_model
from django.test import override_settings

User = get_user_model()

SLA_URL = "https://example.com/sla/v1.0"
SLA_VERSION = "1.0"


class TestCustomExtraFields:
    """
    Tests of the CustomExtraFields model.
    """

    @pytest.mark.skip(
        reason="Placeholder to allow pytest to succeed before real tests are in place."
    )
    def test_placeholder(self):
        """
        TODO: Delete this test once there are real tests.
        """


@pytest.mark.django_db
class TestUserSlaAcceptance:
    """
    Tests of the UserSlaAcceptance model.
    """

    def test_create_sla_acceptance_record(self):
        """Creating a UserSlaAcceptance record stores the expected field values."""
        from custom_extra_fields.models import UserSlaAcceptance

        user = User.objects.create_user(username="testuser", password="password")
        record = UserSlaAcceptance.objects.create(
            user=user,
            sla_version=SLA_VERSION,
            sla_url=SLA_URL,
        )

        assert record.user == user
        assert record.sla_version == SLA_VERSION
        assert record.sla_url == SLA_URL
        assert record.accepted_at is not None

    def test_str_representation(self):
        """The __str__ method includes username, version, and timestamp."""
        from custom_extra_fields.models import UserSlaAcceptance

        user = User.objects.create_user(username="struser", password="password")
        record = UserSlaAcceptance.objects.create(
            user=user,
            sla_version="2.1",
            sla_url=SLA_URL,
        )

        assert "struser" in str(record)
        assert "2.1" in str(record)

    def test_one_record_per_user(self):
        """UserSlaAcceptance is a OneToOneField; a second record for the same user fails."""
        from custom_extra_fields.models import UserSlaAcceptance

        user = User.objects.create_user(username="dupuser", password="password")
        UserSlaAcceptance.objects.create(user=user, sla_version="1.0", sla_url=SLA_URL)

        with pytest.raises(Exception):
            UserSlaAcceptance.objects.create(user=user, sla_version="1.1", sla_url=SLA_URL)


@pytest.mark.django_db
class TestSlaConf:
    """
    Tests of the conf helpers that read SLA settings.
    """

    @override_settings(
        CUSTOM_EXTRA_FIELDS_SLA_URL="https://conf-test.example.com/sla",
        CUSTOM_EXTRA_FIELDS_SLA_VERSION="3.0",
    )
    def test_get_sla_url_from_settings(self):
        """get_sla_url() returns the value configured in settings."""
        from custom_extra_fields.conf import get_sla_url

        assert get_sla_url() == "https://conf-test.example.com/sla"

    @override_settings(
        CUSTOM_EXTRA_FIELDS_SLA_URL="https://conf-test.example.com/sla",
        CUSTOM_EXTRA_FIELDS_SLA_VERSION="3.0",
    )
    def test_get_sla_version_from_settings(self):
        """get_sla_version() returns the value configured in settings."""
        from custom_extra_fields.conf import get_sla_version

        assert get_sla_version() == "3.0"

    def test_get_sla_url_defaults_to_empty(self):
        """get_sla_url() returns '' when the setting is absent."""
        from custom_extra_fields.conf import get_sla_url

        with override_settings():
            # Remove the setting entirely
            from django.conf import settings
            if hasattr(settings, "CUSTOM_EXTRA_FIELDS_SLA_URL"):
                delattr(settings, "CUSTOM_EXTRA_FIELDS_SLA_URL")
            assert get_sla_url() == ""

    def test_get_sla_version_defaults_to_empty(self):
        """get_sla_version() returns '' when the setting is absent."""
        from custom_extra_fields.conf import get_sla_version

        with override_settings():
            from django.conf import settings
            if hasattr(settings, "CUSTOM_EXTRA_FIELDS_SLA_VERSION"):
                delattr(settings, "CUSTOM_EXTRA_FIELDS_SLA_VERSION")
            assert get_sla_version() == ""


class TestCustomExtraFieldsForm:
    """
    Tests of the CustomExtraFieldsForm, focusing on the SLA field.
    """

    @override_settings(
        CUSTOM_EXTRA_FIELDS_SLA_URL=SLA_URL,
        CUSTOM_EXTRA_FIELDS_SLA_VERSION=SLA_VERSION,
    )
    def test_sla_acceptance_field_present(self):
        """The form exposes an 'sla_acceptance' field."""
        from custom_extra_fields.forms import CustomExtraFieldsForm

        form = CustomExtraFieldsForm()
        assert "sla_acceptance" in form.fields

    @override_settings(
        CUSTOM_EXTRA_FIELDS_SLA_URL=SLA_URL,
        CUSTOM_EXTRA_FIELDS_SLA_VERSION=SLA_VERSION,
    )
    def test_sla_acceptance_required(self):
        """The form is invalid when sla_acceptance is not checked."""
        from custom_extra_fields.forms import CustomExtraFieldsForm

        form = CustomExtraFieldsForm(data={})
        assert not form.is_valid()
        assert "sla_acceptance" in form.errors

    @override_settings(
        CUSTOM_EXTRA_FIELDS_SLA_URL=SLA_URL,
        CUSTOM_EXTRA_FIELDS_SLA_VERSION=SLA_VERSION,
    )
    def test_sla_acceptance_widget_contains_url(self):
        """The SLA widget renders a link containing the configured URL."""
        from custom_extra_fields.forms import SlaAcceptanceWidget

        widget = SlaAcceptanceWidget()
        rendered = widget.render("sla_acceptance", False, attrs={"id": "id_sla_acceptance"})
        assert SLA_URL in rendered

    @override_settings(
        CUSTOM_EXTRA_FIELDS_SLA_URL=SLA_URL,
        CUSTOM_EXTRA_FIELDS_SLA_VERSION=SLA_VERSION,
    )
    def test_sla_acceptance_widget_contains_version(self):
        """The SLA widget renders the configured SLA version."""
        from custom_extra_fields.forms import SlaAcceptanceWidget

        widget = SlaAcceptanceWidget()
        rendered = widget.render("sla_acceptance", False, attrs={"id": "id_sla_acceptance"})
        assert SLA_VERSION in rendered
