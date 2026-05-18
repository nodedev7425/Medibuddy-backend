import uuid

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from api.models import User, Device, Box, DeviceToken

class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument(
            "--device-name",
            type=str,
            help="Device name"
        )

        parser.add_argument(
            "--boxes",
            type=int,
            help="Amount of boxes"
        )

        parser.add_argument(
            "--users",
            nargs="+",
            type=uuid.UUID,
            help="User UUIDs"
        )
    
    def handle(self, *args, **options):
     
        # Eingabe

        device_name = options.get("device_name")
        box_amount = options.get("boxes")
        user_ids = options.get("users")

        if not device_name:
            device_name = input("Device name: ").strip()

        if box_amount is None:
            box_amount = self.ask_int("Box amount")

        if not user_ids:
            user_ids = self.ask_user_ids()

        users = User.objects.filter(
            user_id__in=user_ids
        )

        if users.count() != len(user_ids):
            raise CommandError("One or more users do not exist")

        # Verarbeitung

        with transaction.atomic():

            # Device

            device = Device.objects.create(
                name=device_name
            )

            # Users

            for user in users:
                user.devices.add(device)

            # Boxes

            boxes = [
                Box(
                    box_index=i,
                    display_name=f"Box {i + 1}",
                    device=device
                )
                for i in range(box_amount)
            ]

            Box.objects.bulk_create(boxes)

            # Token

            device_token = DeviceToken.objects.create(
                device=device
            )

        # Ausgabe

        self.stdout.write(
            self.style.SUCCESS(
                f"Device created\n"
                f"ID: {device.device_id}\n"
                f"Token: {device_token.token}"
            )
        )

    def ask_int(self, label):

        while True:

            value = input(f"{label}: ").strip()

            try:
                return int(value)

            except ValueError:
                self.stdout.write(
                    self.style.ERROR("Please enter a valid integer")
                )

    def ask_user_ids(self):

        raw = input(
            "User IDs (space separated UUIDs): "
        ).strip()

        ids = []

        for value in raw.split():

            try:
                ids.append(uuid.UUID(value))

            except ValueError:
                raise CommandError(
                    f"Invalid UUID: {value}"
                )

        return ids
