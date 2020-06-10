from django.urls import path
from central_erros.api.views import (ListCreateErrorLogAPIView, 
                                     RetrieveDestroyErrorLogAPIView, 
                                     ArchiveErrorLogAPIView)

app_name = 'api'

urlpatterns = [
    path('logs/', 
         ListCreateErrorLogAPIView.as_view(), 
         name='list-create-logs'),
    path('logs/<int:id>/',
         RetrieveDestroyErrorLogAPIView.as_view(),
         name='get-log'),
    path('logs/<int:id>/archive/',
         ArchiveErrorLogAPIView.as_view(),
         name='archive-log'),
] 
