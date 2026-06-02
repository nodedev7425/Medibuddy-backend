import logging

from dateutil import rrule

from django.db import transaction, IntegrityError
from django.db.models.query import QuerySet

from django.utils import timezone

from api.models import Schedule, Alert, UserAlert, User

logger = logging.getLogger(__name__)


"""
    AlertService
"""
class AlertService:

    """
        Alert exists
    """

    @staticmethod
    def alert_exists(schedule: Schedule, trigger_time) -> bool:

        latest_alert = (
            Alert.objects
            .filter(schedule=schedule)
            .order_by('-trigger_time')
            .first()
        )

        if latest_alert is None:
            return False

        rule = rrule.rrulestr(schedule.rule_string)

        next_occurrence = rule.after(
            latest_alert.trigger_time,
            inc=False
        )

        return (
            next_occurrence is None or
            trigger_time < next_occurrence
        )

    """
        Create alert
    """

    @staticmethod
    def create_alert(schedule_id) -> bool:
        try:
            with transaction.atomic():

                schedule = Schedule.objects.select_related(
                    'box__device'
                ).get(schedule_id=schedule_id)

                alert = Alert.objects.create(schedule=schedule)

                users = User.objects.filter(
                    devices=schedule.box.device
                )

                UserAlert.objects.bulk_create([
                    UserAlert(user=user, alert=alert)
                    for user in users
                ])

            return True

        except Schedule.DoesNotExist:
            logger.warning(
                "Schedule %s does not exist",
                schedule_id
            )

        except IntegrityError as e:
            logger.exception(
                "Database integrity error while creating alert: %s",
                e
            )

        return False
    

"""
    UserAlertService
"""
class UserAlertService:

    """
        Get available Alerts
    """

    @staticmethod
    def get_available_alerts(user: User) -> list[UserAlert]:

        alerts = list(
            UserAlert.objects.filter(
                user=user,
                received__isnull=True
            )
        )

        print(len(alerts))

        if alerts:
            now = timezone.now()

            for user_alert in alerts:
                user_alert.received = now

            UserAlert.objects.bulk_update(
                alerts,
                ['received']
            )

        return alerts