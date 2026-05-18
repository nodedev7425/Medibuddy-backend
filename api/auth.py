from rest_framework import authentication
from rest_framework import exceptions

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