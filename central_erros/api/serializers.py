from rest_framework import serializers

from central_erros.api.models import ErrorLog
from central_erros.accounts.serializers import UserSerializer


class ErrorLogSerializer(serializers.ModelSerializer):
    LEVEL_OPTIONS = ('CRITICAL', 'DEBUG', 'ERROR', 'WARNING', 'INFO')
    ENV_OPTIONS = ('PRODUCTION', 'HOMOLOGATION', 'DEV')

    level = serializers.ChoiceField(choices=LEVEL_OPTIONS)
    env = serializers.ChoiceField(choices=ENV_OPTIONS)
    class Meta:
        model = ErrorLog
        fields = [
            'description', 'source', 'events', 
            'date', 'level', 'env'
        ]


class DetailsErrorLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ErrorLog
        fields = [
            'id', 'user', 'description', 'source', 'details', 
            'events', 'date', 'level', 'env', 'archived'
        ]
