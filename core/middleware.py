from django.conf import settings
from django.shortcuts import redirect


class ForcePrimaryDomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(":")[0]
        primary_domain = "www.wecodewesketch.com"

        # Do nothing in local development
        if settings.DEBUG:
            return self.get_response(request)

        if host != primary_domain:
            return redirect(f"https://{primary_domain}{request.get_full_path()}", permanent=True)

        return self.get_response(request)