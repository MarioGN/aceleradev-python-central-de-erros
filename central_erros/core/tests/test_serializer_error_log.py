from datetime import datetime
from django.test import TestCase

from central_erros.core.models import ErrorLog
from central_erros.core.serializers import ErrorLogSerializer


class ErrorLogSerializerTest(TestCase):
    def setUp(self):
        self.obj = ErrorLog.objects.create(
            source='127.0.0.1',
            description='acceleration.Detail: <not found>',
            details='File "/app/source/core/service.py", line 182, in (*App).Error',
            raised_at=datetime.now()
        )
        self.serializer = ErrorLogSerializer(instance=self.obj)

    def test_serializer_contains_expected_fields(self):
        data = self.serializer.data
        expected = set(['id', 'source', 'description', 'events', 'details', 'raised_at'])
        self.assertEqual(set(data.keys()), expected)

    def test_source_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['source'], '127.0.0.1')

    def test_description_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['description'], 'acceleration.Detail: <not found>')

    def test_details_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['details'], 'File "/app/source/core/service.py", line 182, in (*App).Error')

    def test_events_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['events'], 1)
