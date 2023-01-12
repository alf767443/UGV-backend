from rest_framework import serializers
from ActionsApplication.models import *

class ActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Actions
        fields=('__all__')

class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model=Queue
        fields=('__all__')
        depth = 1