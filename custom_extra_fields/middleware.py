"""
Middleware for custom_extra_fields.
"""

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from custom_extra_fields.conf import get_sla_version

# Paths that must never be intercepted.
# Add any additional paths your deployment needs (e.g. password-reset URLs).
EXEMPT_URL_PREFIXES = (
    "/sla/",        # the acceptance page itself — avoids redirect loop
    "/logout",      # always allow logout
    "/admin/",      # Django admin has its own auth
    "/static/",     # static assets
    "/api/",        # REST/API clients cannot follow an HTML redirect
    "/auth/",       # Python Social Auth login + OIDC callback URLs;
                    # an already-authenticated user can hit these during
                    # silent re-auth or token refresh — intercepting them
                    # would break the OIDC flow mid-flight.
)


class SlaAcceptanceMiddleware(MiddlewareMixin):
    """
    Redirect authenticated users to the SLA acceptance page whenever the
    version they last accepted no longer matches ``CUSTOM_EXTRA_FIELDS_SLA_VERSION``
    in settings.

    To enable, add to ``MIDDLEWARE`` in settings **after**
    ``django.contrib.auth.middleware.AuthenticationMiddleware``::

        "custom_extra_fields.middleware.SlaAcceptanceMiddleware"
    """

    def process_request(self, request):
        if not request.user.is_authenticated:
            return None

        path = request.path_info
        if any(path.startswith(prefix) for prefix in EXEMPT_URL_PREFIXES):
            return None

        current_version = get_sla_version()
        if not current_version:
            # SLA version not configured — nothing to enforce.
            return None

        if not self._has_accepted_current_version(request.user, current_version):
            acceptance_url = f"/sla/accept/?next={path}"
            return redirect(acceptance_url)

        return None

    @staticmethod
    def _has_accepted_current_version(user, current_version):
        """Return True if the user has already accepted the current SLA version."""
        try:
            return user.sla_acceptance.sla_version == current_version
        except Exception:  # pylint: disable=broad-except
            # No acceptance record exists yet.
            return False
