from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, ObtainJSONWebToken

from central_erros.accounts.views import RegisterAPIView
from central_erros.accounts.serializers import CustomJWTSerializer

app_name = 'accounts'

urlpatterns = [
    path('login/', 
         ObtainJSONWebToken.as_view(serializer_class=CustomJWTSerializer),
         name='login'),
    path('register/',
         RegisterAPIView.as_view(),
         name='register')
]
