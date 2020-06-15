from django.urls import path
from central_erros.api import views
app_name = 'api'

urlpatterns = [
    path('logs/', 
         views.ListCreateErrorLogAPIView.as_view(), 
         name='list-create-logs'),
    path('logs/<int:id>/',
         views.RetrieveArchiveDestroyErrorLogAPIView.as_view(),
         name='get-archive-delete-logs'),
] 
