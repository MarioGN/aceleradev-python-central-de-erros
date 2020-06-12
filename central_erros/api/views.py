from django.http import Http404
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from central_erros.api.models import ErrorLog
from central_erros.api.serializers import ErrorLogSerializer, DetailsErrorLogSerializer


class ListCreateErrorLogAPIView(ListCreateAPIView):
    serializer_class = ErrorLogSerializer
    search_fields = ('level', 'description', 'source')
    ordering_fields = ('level', '-level', 'events', '-events')

    def get_queryset(self):
        request = self.request
        qs = ErrorLog.objects.all()
        qs = self._filter(self.request, qs)
        return qs

    def _filter(self, request, queryset):
        env = request.GET.get('env', None)
        ordering = request.GET.get('ordering', None)
        search_field = request.GET.get('field', None)
        search = request.GET.get('search', None)

        if env is not None:
            queryset = queryset.filter(env__iexact=env)
        if ordering is not None and ordering in self.ordering_fields:
            queryset = queryset.order_by(ordering)
        if search_field is not None and search_field in self.search_fields and search is not None:
            field_query = {f'{search_field}__icontains': search}
            queryset = queryset.filter(**field_query)

        return queryset


class RetrieveDestroyErrorLogAPIView(RetrieveDestroyAPIView):
    queryset = ErrorLog.objects.all()
    serializer_class = DetailsErrorLogSerializer
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
