from datetime import datetime
from django.test import TestCase

from central_erros.core.models import ErrorLog
from central_erros.core.serializers import ErrorLogSerializer


class ErrorLogSerializerTestCase(TestCase):
    def setUp(self):
        self.obj = ErrorLog.objects.create(
            source='127.0.0.1',
            description='acceleration.Detail: <not found>',
            details='File "/app/source/core/service.py", line 182, in (*App).Error',
            raised_at=datetime.now()
        )
        self.data = ErrorLogSerializer(instance=self.obj).data

    def test_serializer_should_contains_expected_fields(self):
        expected = set(['id', 'source', 'description', 'events', 'details', 'raised_at'])
        self.assertEqual(expected, set(self.data.keys()))

    def test_source_field_content(self):
        self.assertEqual(self.obj.source, self.data['source'])

    def test_description_field_content(self):
        self.assertEqual(self.obj.description, self.data['description'])
        
    def test_details_field_content(self):
        self.assertEqual(self.obj.details, self.data['details'])
        
    def test_events_field_content(self):
        self.assertEqual(self.obj.events, self.data['events'])

    def test_raised_at_field_is_serialized(self):
        self.assertIsInstance(self.data['raised_at'], str)
