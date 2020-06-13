from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from central_erros.api.models import ErrorLog
from central_erros.api.serializers import ErrorLogSerializer, DetailsErrorLogSerializer
from .utils import JWTAuthenticatedTestCase


class GETDetailErrorLogAPIView(JWTAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self._make_logs(quantity=6)

    def test_get_single_log_should_return_status_200(self):
        url = reverse('api:get-delete-logs', kwargs={'id': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_single_invalid_log_should_return_status_404(self):
        url = reverse('api:get-delete-logs', kwargs={'id': 999})
        response = self.client.get(url, format='json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_get_serialized_data(self):
        obj = ErrorLog.objects.get(pk=1)
        serializer = DetailsErrorLogSerializer(obj)
        url = reverse('api:get-delete-logs', kwargs={'id': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.data, serializer.data)


class DELETEDetailErrorLogAPIView(JWTAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self._make_logs()

    def test_delete_log_should_return_status_204(self):
        url = reverse('api:get-delete-logs', kwargs={'id': 1})
        response = self.client.delete(url, format='json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_get_invalid_log_should_return_status_404(self):
        url = reverse('api:get-delete-logs', kwargs={'id': 999})
        response = self.client.delete(url, format='json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_delete_errorlog_with_invalid_credentials_should_return_403(self):
        user_data = {'username': 'anotheruser', 'email': 'anotheruser@email.com', 'password': 'secret123'}
        self._perform_create_user_and_jwt_authenticate(user_data)
        url = reverse('api:get-delete-logs', kwargs={'id': 1})
        response = self.client.delete(url, format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
