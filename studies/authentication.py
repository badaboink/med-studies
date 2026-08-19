from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class FrontendAuthentication(BaseAuthentication):

    def authenticate(self, request):
        print(request.headers)

        api_key = request.headers.get("X-API-Key")
        if not api_key:
            raise AuthenticationFailed(
                "Missing API key."
            )

        if api_key != settings.FRONTEND_API_KEY:
            raise AuthenticationFailed(
                "Invalid API key."
            )

        return (None, None)