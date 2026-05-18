import uuid
import random

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from django.core.management import call_command

from django.utils import timezone
from dateutil.rrule import rrule, MONTHLY

from api.models import User, Box, Schedule

class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument("--test-user",
            type=uuid.UUID,
            help="Test User UUID")

    def handle(self, *args, **options):

        test_user_id = options.get('test-user')

        if test_user_id is None:
            test_user_id = self.ask_user_id()

        try:
            test_user = User.objects.get(
                user_id=test_user_id
            )
        except User.DoesNotExist:
            raise CommandError(
                f"User not found: {test_user_id}"
            )
        
        if test_user.devices.filter(
            name="Demo Device"
        ).exists():
            raise CommandError(
                f"User already has a demo device"
            )

        # Device

        call_command(
            "create_device",
            device_name="Demo Device",
            boxes=3,
            users=[
                f"{test_user.user_id}"
            ]
        )

        # Schedules

        demo_device = test_user.devices.get(
            name="Demo Device"
        )

        with transaction.atomic():

            boxes = Box.objects.filter(device=demo_device)

            for box in boxes:
                Schedule.objects.create(
                    box=box, 
                    start_time=timezone.now(), 
                    rule_string=str(
                        rrule(
                            freq=MONTHLY,
                            count=random.randint(1, 12),
                            dtstart=timezone.now()
                        )
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                "\nSchedules created"
            )
        )


    def ask_user_id(self):

        raw = input("Test User ID: ")

        try:
            id = uuid.UUID(raw)

        except ValueError:
            raise CommandError(
                f"Invalid UUID: {raw}"
            )

        return id
