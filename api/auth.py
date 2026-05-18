from rest_framework import authentication
from rest_framework import exceptions

from drf_spectacular.extensions import OpenApiAuthenticationExtension

from .models import DeviceToken

class DeviceAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        token = request.headers.get("X-API-KEY")

        if not token:
            return None

        try:
            device_token = DeviceToken.objects.select_related("device").get(
                token=token
            )
        except DeviceToken.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid token")

        return (device_token.device, device_token)
    

class DeviceAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'api.auth.DeviceAuthentication'
    name = 'ApiTokenAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'X-API-KEY',
        }