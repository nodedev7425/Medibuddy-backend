from rest_framework import viewsets

from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.utils.dateparse import parse_datetime
from django.utils import timezone

from api.models import Device, Schedule, Box
from api.auth import DeviceAuthentication
from api.serializers import ScheduleSerializer
 
"""
    Schedules
"""
class ScheduleConfigApiView(APIView):

    authentication_classes = [DeviceAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ScheduleSerializer

    """
        GET Schedules for authenticated device
    """
    def get(self, request, format=None):
        
        last_sync = request.GET.get("last_sync")
        force = request.GET.get("force", "false").lower() == "true"

        if not last_sync:
            return Response(
                {"error": "Missing required GET parameter 'last_sync'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        parsed_last_sync = parse_datetime(last_sync)

        if parsed_last_sync is None:
            return Response(
                {"error": "Invalid datetime format for 'last_sync'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if timezone.is_naive(parsed_last_sync):
            parsed_last_sync = timezone.make_aware(parsed_last_sync)

        device = request.user

        if force or device.sync_timestamp is None or device.sync_timestamp > parsed_last_sync:

            schedules = Schedule.objects.filter(
                box__device=device
            ).select_related("box")

            serializer = ScheduleSerializer(schedules, many=True)

            device.sync_timestamp = timezone.now()
            device.save(update_fields=["sync_timestamp"])

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_204_NO_CONTENT)

        
"""
    Alerts
"""
class AlertApiView(GenericAPIView):

    authentication_classes = [DeviceAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        pass
     
