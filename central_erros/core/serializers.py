from rest_framework.serializers import ModelSerializer

from central_erros.core.models import ErrorLog


class ErrorLogSerializer(ModelSerializer):
    class Meta:
        model = ErrorLog
        fields = [
            'id', 'source', 'description', 
            'events', 'details', 'raised_at'
        ]
