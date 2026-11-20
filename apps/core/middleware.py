from django.conf import settings


class SecurityHeadersMiddleware:
    """Headers that Django's defaults do not add, without breaking API docs."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response.headers.setdefault(
            "Permissions-Policy",
            "camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()",
        )
        # Swagger/ReDoc are a third-party UI; the site policy would block their
        # inline bootstrap. They already send noindex and are not public pages.
        if not request.path.startswith("/api/"):
            response.headers.setdefault(
                "Content-Security-Policy",
                (
                    "default-src 'self'; "
                    "base-uri 'self'; "
                    "object-src 'none'; "
                    "frame-ancestors 'none'; "
                    "form-action 'self'; "
                    "img-src 'self' data: https:; "
                    "font-src 'self' https://fonts.gstatic.com data:; "
                    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
                    "script-src 'self' 'unsafe-inline'; "
                    "connect-src 'self'; "
                    "frame-src https://www.google.com https://maps.google.com; "
                    "upgrade-insecure-requests"
                ),
            )
        return response