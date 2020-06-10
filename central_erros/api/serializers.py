from rest_framework import serializers

from central_erros.api.models import ErrorLog


class ErrorLogSerializer(serializers.ModelSerializer):
    LEVEL_OPTIONS = ('CRITICAL', 'DEBUG', 'ERROR', 'WARNING', 'INFO')
    ENV_OPTIONS = ('PRODUÇÃO', 'HOMOLOGAÇÃO', 'DEV')

    level = serializers.ChoiceField(choices=LEVEL_OPTIONS)
    env = serializers.ChoiceField(choices=ENV_OPTIONS)

    class Meta:
        model = ErrorLog
        fields = [
            'description', 'source', 'details', 'events', 
            'date', 'level', 'env'
        ]


class DetailsErrorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorLog
        fields = [
            'id', 'description', 'source', 'details', 'events', 
            'date', 'level', 'env', 'archived'
        ]
