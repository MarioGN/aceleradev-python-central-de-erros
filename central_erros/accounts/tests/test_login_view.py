from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import authenticate, get_user_model

from rest_framework import status
from rest_framework.test import APIClient


User = get_user_model()


class JWTLoginWithEmailAndPasswordTestCase(TestCase):
    def setUp(self):
        self.data = {'username': 'apiuser', 'email': 'apiuser@email.com', 'password': 'passjwt01'}
        User.objects.create_user(**self.data)
        self.url = reverse('accounts:login')
        self.client = APIClient()

    def test_jwt_login_with_email_and_password_should_return_status_200(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_invalid_credentials_jwt_login_with_email_and_password_should_return_status_400(self):
        self.data['password'] = 'wrongpass123'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
