"""
Middleware for custom_extra_fields.
"""

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from custom_extra_fields.conf import get_sla_version

# Paths that must never be intercepted.
# Add any additional paths your deployment needs (e.g. password-reset URLs).
EXEMPT_URL_PREFIXES = (
    "/sla/",           # the acceptance page itself — avoids redirect loop
    "/logout",         # always allow logout
    "/login",          # login endpoints and pages
    "/login_refresh",  # MFE JWT cookie refresh endpoint
    "/admin/",         # Django admin has its own auth
    "/static/",        # static assets
    "/media/",         # media files
    "/favicon.ico",    # browser favicon
    "/api/",           # REST/API clients cannot follow an HTML redirect
    "/user_api/",      # User API endpoints (registration, account settings)
    "/oauth2/",        # OAuth2 token and authorization endpoints
    "/auth/",          # Python Social Auth login + OIDC callback URLs
    "/authn/",         # Auth MFE routes
    "/heartbeat",      # health check endpoints
    "/i18n/",          # language switcher
    "/csrf/",          # CSRF endpoints
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

        # Only redirect standard browser GET/HEAD page navigations.
        # Intercepting POST/PUT/DELETE or AJAX/API calls breaks form submissions,
        # token refresh flows (e.g. /login_refresh), and background data fetches.
        if request.method not in ("GET", "HEAD"):
            return None

        # Do not redirect AJAX or JSON-accepting API requests
        if (
            request.headers.get("x-requested-with") == "XMLHttpRequest"
            or "application/json" in request.headers.get("accept", "")
        ):
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
