import sys
import os

from django.apps import AppConfig
from django.conf import settings

from tasks.clean_task import start_task

class TasksConfig(AppConfig):
    name = 'tasks'

    def ready(self):
       
       skip = {'migrate', 'makemigrations', 'collectstatic', 'shell'}

       if len(sys.argv) > 1 and sys.argv[1] in skip:
            return
       
       if settings.DEBUG and os.environ.get("RUN_MAIN") == "true":
        start_task()

