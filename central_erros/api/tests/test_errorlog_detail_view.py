from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from central_erros.api.models import ErrorLog
from central_erros.api.serializers import ErrorLogSerializer


VALID_PAYLOAD = {
    "description": "acceleration.Detail: <not found>",   
    "source": "127.0.0.1",
    "details": "File \"/app/source/core/service.py\", line 182, in (*App).Error",
    "events": "10",
    "date": "2020-06-04T13:41:28+00:00",
    "level": "ERROR",
    "env": "DEV",
}


class GETDetailErrorLogAPIView(TestCase):
    def setUp(self):
        for i in range(1, 6):
            VALID_PAYLOAD['description'] = f'Error Log {i}'
            ErrorLog.objects.create(**VALID_PAYLOAD)

        self.client = APIClient()

    def test_get_single_log_should_return_status_200(self):
        url = reverse('api:get-log', kwargs={'id': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_single_invalid_log_should_return_status_404(self):
        url = reverse('api:get-log', kwargs={'id': 999})
        response = self.client.get(url, format='json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_get_serialized_data(self):
        obj = ErrorLog.objects.get(pk=1)
        serializer = ErrorLogSerializer(obj)
        url = reverse('api:get-log', kwargs={'id': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.data, serializer.data)
