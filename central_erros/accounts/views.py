from django.shortcuts import render
from django.contrib.auth import authenticate, get_user_model

from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from central_erros.accounts.serializers import UserRegisterSerializer


User = get_user_model()


class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]
