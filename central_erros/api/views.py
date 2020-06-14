from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from central_erros.api.models import ErrorLog
from central_erros.api.serializers import ErrorLogSerializer, DetailsErrorLogSerializer
from central_erros.api.permissions import IsOwnerOrReadOnly


class ListCreateErrorLogAPIView(ListCreateAPIView):
    serializer_class = ErrorLogSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        query_params = self.request.query_params
        queryset = ErrorLog.objects.filter_logs(query_params)
        return queryset


class RetrieveDestroyErrorLogAPIView(RetrieveDestroyAPIView):
    queryset = ErrorLog.objects.all()
    serializer_class = DetailsErrorLogSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'id'


class ArchiveErrorLogAPIView(APIView):
    permission_classes = permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self, id):
        obj = get_object_or_404(ErrorLog, id=id)
        self.check_object_permissions(self.request, obj)
        return obj

    def patch(self, request, id):
        obj = self.get_object(id)
        obj.archive()
        return Response(status=status.HTTP_204_NO_CONTENT)
