from rest_framework import serializers

from api.models import Box, Schedule

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
    rule_string = serializers.CharField(max_length=255)
    box = BoxSerializer()

    class Meta:
        model = Schedule