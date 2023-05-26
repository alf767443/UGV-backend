#!/usr/bin/env python3

from django.apps import AppConfig


class MongodbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MongoDB'
