from django.http import Http404
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from central_erros.api.models import ErrorLog
from central_erros.api.serializers import ErrorLogSerializer


class ListCreateErrorLogAPIView(ListCreateAPIView):
    queryset = ErrorLog.objects.all()
    serializer_class = ErrorLogSerializer


class RetrieveDestroyErrorLogAPIView(RetrieveDestroyAPIView):
    queryset = ErrorLog.objects.all()
    serializer_class = ErrorLogSerializer
    lookup_field = 'id'


class ArchiveErrorLogAPIView(APIView):
    def get_object(self, id):
        try:
            return ErrorLog.objects.get(id=id)
        except ErrorLog.DoesNotExist:
            raise Http404

    def patch(self, request, id):
        obj = self.get_object(id)
        obj.archive()
        obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
