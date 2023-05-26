#!/usr/bin/env python3

from django.apps import AppConfig
import threading
from .task import execute_background_task


class MongodbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MongoDB'
    
    def ready(self):
            # Create a thread and start it
            thread = threading.Thread(target=execute_background_task)
            thread.daemon = True
            thread.start()