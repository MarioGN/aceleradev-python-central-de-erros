from django.urls import path
from central_erros.api.views import ListCreateErrorLogAPIView

app_name = 'api'

urlpatterns = [
    path('logs/', 
         ListCreateErrorLogAPIView.as_view(), 
         name='list-create-logs'),
]
