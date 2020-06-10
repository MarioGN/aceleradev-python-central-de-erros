from django.urls import path
from central_erros.api.views import ListCreateErrorLogAPIView, DetailErrorLogAPIView

app_name = 'api'

urlpatterns = [
    path('logs/', 
         ListCreateErrorLogAPIView.as_view(), 
         name='list-create-logs'),
    path('logs/<int:id>/',
         DetailErrorLogAPIView.as_view(),
         name='get-log'),
]
