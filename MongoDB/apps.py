#!/usr/bin/env python3

from django.apps import AppConfig
import threading
from .task import execute_background_task


class MongodbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MongoDB'

class BackgroundTaskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backgroudTask'

    def ready(self):
        # Crie uma thread e inicie-a
        thread = threading.Thread(target=execute_background_task)
        thread.daemon = True
        thread.start()
