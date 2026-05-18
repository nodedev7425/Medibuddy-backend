from rest_framework import serializers

from api.models import Box, Schedule, Alert, UserAlert

"""
    BoxSerializer
"""
class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ['box_id', 'box_index']

"""
    ScheduleSerializer
"""
class ScheduleSerializer(serializers.Serializer):

    schedule_id = serializers.UUIDField(read_only=True) 
    display_name = serializers.CharField()
    rule_string = serializers.CharField(max_length=255)
    box = BoxSerializer()

    class Meta:
        model = Schedule

"""
    AlertSerializer
"""
class AlertSerializer(serializers.Serializer):

    alert_id = serializers.UUIDField(read_only=True) 
    schedule = ScheduleSerializer()
    trigger_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Alert

"""
    UserAlertSerializer
"""
class UserAlertSerializer(serializers.Serializer):
    
    user_alert_id = serializers.UUIDField(read_only=True) 
    alert = AlertSerializer()

    class Meta:
        model = UserAlert