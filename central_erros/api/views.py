from rest_framework.generics import ListCreateAPIView

from central_erros.api.models import ErrorLog
from central_erros.api.serializers import ErrorLogSerializer


class ListCreateErrorLogAPIView(ListCreateAPIView):
    queryset = ErrorLog.objects.all()
    serializer_class = ErrorLogSerializer
