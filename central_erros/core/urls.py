from django.urls import path
from central_erros.core.views import CreateErrorLogAPIView

app_name = 'core'

urlpatterns = [
    path('logs/', CreateErrorLogAPIView.as_view(), name='post-new-log'),
]
