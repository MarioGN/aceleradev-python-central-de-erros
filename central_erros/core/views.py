from rest_framework.generics import CreateAPIView, ListAPIView

from central_erros.core.models import ErrorLog
from central_erros.core.serializers import ErrorLogSerializer


class CreateErrorLogAPIView(CreateAPIView):
    queryset = ErrorLog.objects.all()
    serializer_class = ErrorLogSerializer
