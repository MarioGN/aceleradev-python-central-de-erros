from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from central_erros.api.models import ErrorLog
from central_erros.api.serializers import ErrorLogSerializer
from .utils import JWTAuthenticatedTestCase


class PACTCHArchiveErrorLogAPIView(JWTAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self._make_logs(quantity=6)

    def test_patch_archive_errorlog_should_return_status_204(self):
        url = reverse('api:archive-logs', kwargs={'id': 1})
        response = self.client.patch(url, format='json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_invalid_patch_archive_errorlog_should_return_status_404(self):
        url = reverse('api:archive-logs', kwargs={'id': 999})
        response = self.client.patch(url, format='json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_error_log_should_be_archived(self):
        obj = ErrorLog.objects.get(pk=2)
        self.assertFalse(obj.archived)
        url = reverse('api:archive-logs', kwargs={'id': 2})
        response = self.client.patch(url, format='json')
        obj.refresh_from_db()
        self.assertTrue(obj.archived)
  