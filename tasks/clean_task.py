import logging
import os
import sys

from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from apscheduler.schedulers.background import BackgroundScheduler

from api.models import Alert, UserAlert

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

ALERT_TIMEOUT = int(os.getenv('ALERT_TIMEOUT', 172800))
WIPE_INTERVAL = int(os.getenv('WIPE_INTERVAL', 60))

_task = None

def task():
    try:
        logger.info("Starting to delete outdated alerts...")

        amount = 0
        cutoff = timezone.now() - timedelta(
            seconds=ALERT_TIMEOUT
        )

        for alert in Alert.objects.filter(
            trigger_time__lt=cutoff
        ):
            user_alerts = UserAlert.objects.filter(
                alert=alert
            )

            all_received = (
                user_alerts.exists() and
                all(
                    ua.received is not None
                    for ua in user_alerts
                )
            )

            if all_received:
                amount += 1
                alert.delete()

        logger.info(
            "%s alerts were deleted at this wipe.",
            amount
        )

    except Exception:
        logger.exception("Cleanup failed")


def start_task():

    global _task

    if _task and _task.running:
            return
    
    _task = BackgroundScheduler(timezone='Europe/Berlin')

    _task.add_job(
         task,
         'interval',
         name='User alert cleaner',
         minutes=WIPE_INTERVAL,
         max_instances=1
    )

    _task.start()