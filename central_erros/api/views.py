from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView

from central_erros.api.models import ErrorLog
from central_erros.api.serializers import ErrorLogSerializer


class ListCreateErrorLogAPIView(ListCreateAPIView):
    queryset = ErrorLog.objects.all()
    serializer_class = ErrorLogSerializer


class RetrieveDestroyErrorLogAPIView(RetrieveDestroyAPIView):
    queryset = ErrorLog.objects.all()
    serializer_class = ErrorLogSerializer
    lookup_field = 'id'
