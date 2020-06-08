from django.urls import path
from central_erros.core.views import ListCreateErrorLogsAPIView

app_name = 'core'

urlpatterns = [
    path('logs/', 
         ListCreateErrorLogsAPIView.as_view(), 
         name='list-create-logs'),
]
