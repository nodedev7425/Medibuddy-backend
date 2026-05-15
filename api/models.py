from django.db import models

import uuid

from django.contrib.auth.models import AbstractUser

from django.utils import timezone

class Device(models.Model): 
    
    device_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False 
    ) 
    
    name = models.TextField( 
        max_length=255, 
        blank=False 
    ) 
    
    registered_at = models.DateTimeField(
        default=timezone.now, 
        editable=False
    ) 
    
    sync_timestamp = models.DateTimeField()


class User(AbstractUser): 
    
    user_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False 
    )
    
    devices = models.ManyToManyField( 
        Device, 
        related_name="users", 
        blank=True 
    )

"""
    Box
"""
class Box(models.Model):

    box_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    device = models.ForeignKey(
        "Device",
        on_delete=models.CASCADE,
        related_name='boxes'
    )


"""
    Schedule
"""
class Schedule(models.Model):

    schedule_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    box = models.ForeignKey(
        Box,
        on_delete=models.CASCADE,
        related_name='schedules'
    )

    start_time = models.DateTimeField()

    rule_string = models.CharField(
        max_length=255
    )

"""
    Alert
"""
class Alert(models.Model):

    alert_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.CASCADE,
        related_name='alerts'
    )

    trigger_time = models.DateTimeField(
        default=timezone.now,
        editable=False
    )

"""
    UserAlert
"""
class UserAlert(models.Model):

    user_alert_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name='user_alerts'
    )

    alert = models.ForeignKey(
        Alert,
        on_delete=models.CASCADE,
        related_name='user_alerts'
    )

    received = models.DateTimeField(
        null=True,
        blank=True
    )