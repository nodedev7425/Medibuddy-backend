import logging
import sys

from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

_task = None

def task():
    logging.info('test')  


def start_task():

    global _task

    if _task and _task.running:
            return
    
    _task = BackgroundScheduler(timezone='Europe/Berlin')

    _task.add_job(
         task,
         'interval',
         name='User alert cleaner',
         minutes=getattr(60, 'WIPE_INTERVAL'),
         max_instances=1
    )

    _task.start()