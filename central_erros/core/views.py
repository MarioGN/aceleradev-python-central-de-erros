from rest_framework.generics import ListCreateAPIView

from central_erros.core.models import ErrorLog
from central_erros.core.serializers import ErrorLogSerializer


class ListCreateErrorLogsAPIView(ListCreateAPIView):
    queryset = ErrorLog.objects.all()
    serializer_class = ErrorLogSerializer
