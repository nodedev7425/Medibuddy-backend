from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from django.utils.dateparse import parse_datetime
from django.utils import timezone

from api.models import Schedule, Alert, Device, Box, User
from api.services import AlertService, UserAlertService
from api.auth import DeviceAuthentication
from api.serializers import ScheduleSerializer, UserAlertSerializer
 


"""
    Schedules
"""
class ScheduleConfigApiView(GenericAPIView):

    authentication_classes = [DeviceAuthentication]
    permission_classes = [IsAuthenticated]

    """
        GET Schedules for authenticated device
    """

    @extend_schema(
        summary="Get schedules for authenticated device",
        description="Returns all schedules if synchronization is required.",
        parameters=[
            OpenApiParameter(
                name='last_sync',
                type=OpenApiTypes.DATETIME,
                location=OpenApiParameter.QUERY,
                required=True,
                description='Last synchronization timestamp'
            ),
            OpenApiParameter(
                name='force',
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                required=False,
                description='Force full sync'
            ),
        ],
        responses={
            200: ScheduleSerializer(many=True),
            204: OpenApiResponse(description="No updates available"),
            400: OpenApiResponse(description="Invalid request"),
        },
        tags=["Schedules"]
    )

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
            device.save(update_fields=['sync_timestamp'])

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_204_NO_CONTENT)

        
"""
    Alerts
"""
class AlertApiView(GenericAPIView):

    authentication_classes = [DeviceAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Conditional trigger alert for missed schedule",
        description="Conditional trigger alert for missed schedule",
        parameters=[
            OpenApiParameter(
                name='schedule_id',
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.QUERY,
                required=True,
                description='The missed schedule'
            ),
        ],
        responses={
            400: OpenApiResponse(description="Invalid request"),
        },
        tags=["Alerts"]
    )

    def get(self, request, format=None):
        
        schedule_id = request.GET.get('schedule_id')
     
        if not schedule_id:
            return Response(
                {"error": "Missing required GET parameter 'schedule_id'"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:    
            schedule = Schedule.objects.get(
                schedule_id=schedule_id
            )
        except Schedule.DoesNotExist:
            return Response(
                {"error": f"No schedule with ID '{schedule_id}' found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        trigger_time = timezone.now()

        if AlertService.alert_exists(schedule, trigger_time):
            return Response(status=status.HTTP_409_CONFLICT) 
            
        if not AlertService.create_alert(schedule_id):
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_201_CREATED)


"""
    UserAlert
"""
class UserAlertApiView(GenericAPIView):

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Conditional trigger alert for missed schedule",
        description="Conditional trigger alert for missed schedule",
        tags=["Alerts"]
    )

    def get(self, request, format=None):

        alerts = UserAlertService.get_available_alerts(request.user)

        if alerts:
            serializer = UserAlertSerializer(alerts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_204_NO_CONTENT)


from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def devices(request):
    devices_qs = request.user.devices.all()
    print("USER:", request.user)
    print("DEVICES:", list(devices_qs))
    return render(request, "devices.html", {"devices": devices_qs})

@login_required
def device_detail(request, device_id):
    device = Device.objects.get(device_id=device_id)
    boxes = device.boxes.all()

    return render(request, "device.html", {
        "device": device,
        "boxes": boxes
    })


@login_required
def box_detail(request, device_id, box_id):
    box = Box.objects.get(box_id=box_id)
    schedules = box.schedules.all()

    return render(request, "box.html", {
        "box": box,
        "schedules": schedules
    })