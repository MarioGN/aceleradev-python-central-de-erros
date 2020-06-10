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


class PACTCHArchiveErrorLogAPIView(TestCase):
    def setUp(self):
        for i in range(1, 6):
            VALID_PAYLOAD['description'] = f'Error Log {i}'
            ErrorLog.objects.create(**VALID_PAYLOAD)

        self.client = APIClient()

    def test_patch_archive_errorlog_should_return_status_204(self):
        url = reverse('api:archive-log', kwargs={'id': 1})
        response = self.client.patch(url, format='json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_invalid_patch_archive_errorlog_should_return_status_404(self):
        url = reverse('api:archive-log', kwargs={'id': 999})
        response = self.client.patch(url, format='json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_error_log_should_be_archived(self):
        obj = ErrorLog.objects.get(pk=2)
        self.assertFalse(obj.arquivado)

        url = reverse('api:archive-log', kwargs={'id': 2})
        response = self.client.patch(url, format='json')
        obj.refresh_from_db()
        self.assertTrue(obj.arquivado)

    

