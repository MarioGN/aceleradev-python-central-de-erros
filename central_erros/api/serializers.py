from django.urls import reverse

from rest_framework import serializers

from central_erros.api.models import ErrorLog
from central_erros.accounts.serializers import UserSerializer


class ErrorLogSerializer(serializers.ModelSerializer):
    LEVEL_OPTIONS = ('CRITICAL', 'DEBUG', 'ERROR', 'WARNING', 'INFO')
    ENV_OPTIONS = ('PRODUCTION', 'HOMOLOGATION', 'DEV')

    level = serializers.ChoiceField(choices=LEVEL_OPTIONS)
    env = serializers.ChoiceField(choices=ENV_OPTIONS)
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ErrorLog
        fields = [
            'uri', 'description', 'source', 'events', 
            'date', 'level', 'env'
        ]

    def get_uri(self, obj):
        return reverse('api:get-delete-logs', kwargs={'id': obj.id})


class DetailsErrorLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ErrorLog
        fields = [
            'id', 'user', 'description', 'source', 'details', 
            'events', 'date', 'level', 'env', 'archived'
        ]
