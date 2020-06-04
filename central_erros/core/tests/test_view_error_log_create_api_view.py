from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from central_erros.core.models import ErrorLog


class ErrorLogCreateAPIViewTest(TestCase):
    def setUp(self):
        self.valid_payload = {
            "source": "127.0.0.1",
            "description": "acceleration.Detail: <not found>",
            "details": "File \"/app/source/core/service.py\", line 182, in (*App).Error",
            "raised_at": "2020-06-04T13:41:28+00:00"
        }
        self.client = APIClient()

    def test_post_create_error_log_status(self):
        response = self.client.post(reverse('core:post-new-log'), self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_post_create_error_log(self):
        response = self.client.post(reverse('core:post-new-log'), self.valid_payload)
        self.assertEqual(len(ErrorLog.objects.all()), 1)

    def test_post_create_invalid_payload_error_log(self):
        response = self.client.post(reverse('core:post-new-log'), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_create_invalid_payload_without_source(self):
        self.valid_payload.pop('source')
        response = self.client.post(reverse('core:post-new-log'), self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_post_create_source_is_required(self):
        self.valid_payload.pop('source')
        response = self.client.post(reverse('core:post-new-log'), self.valid_payload)
        self.assertIn("required", response.data['source'][0].code)

    def test_post_create_invalid_payload_without_description(self):
        self.valid_payload.pop('description')
        response = self.client.post(reverse('core:post-new-log'), self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_post_create_description_is_required(self):
        self.valid_payload.pop('description')
        response = self.client.post(reverse('core:post-new-log'), self.valid_payload)
        self.assertIn("required", response.data['description'][0].code)

    def test_post_create_invalid_payload_without_details(self):
        self.valid_payload.pop('details')
        response = self.client.post(reverse('core:post-new-log'), self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_post_create_details_is_required(self):
        self.valid_payload.pop('details')
        response = self.client.post(reverse('core:post-new-log'), self.valid_payload)
        self.assertIn("required", response.data['details'][0].code)

    def test_post_create_invalid_payload_without_raised_at(self):
        self.valid_payload.pop('raised_at')
        response = self.client.post(reverse('core:post-new-log'), self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_post_create_raised_at_is_required(self):
        self.valid_payload.pop('raised_at')
        response = self.client.post(reverse('core:post-new-log'), self.valid_payload)
        self.assertIn("required", response.data['raised_at'][0].code)
