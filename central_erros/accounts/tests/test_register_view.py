from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient


class RegisterUserTestCase(TestCase):
    def setUp(self):
        self.data = {
            'username': 'apiuser', 
            'email': 'apiuser@email.com', 
            'password': 'passjwt01',
            'password2': 'passjwt01'}
        self.url = reverse('accounts:register')
        self.response = self.client.post(self.url, self.data, format='json')
        self.client = APIClient()

    def test_post_register_should_return_status_200(self):
        self.assertEqual(status.HTTP_201_CREATED, self.response.status_code)

    def test_post_register_same_user_should_return_status_400(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
