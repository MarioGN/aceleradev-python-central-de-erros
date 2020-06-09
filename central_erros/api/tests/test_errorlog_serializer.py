from django.test import TestCase
from django.utils import timezone

from central_erros.api.models import ErrorLog
from central_erros.api.serializers import ErrorLogSerializer


class ErrorLogSerializerTestCase(TestCase):
    def setUp(self):
        self.obj = ErrorLog.objects.create(
            description='acceleration.Detail: <not found>',
            source='127.0.0.1',
            details='File "/app/source/core/service.py", line 182, in (*App).Error',
            events=10,
            date=timezone.now(),
            level='ERROR',
            env='DEV',
            arquivado=False,
        )

        self.data = ErrorLogSerializer(instance=self.obj).data
    
    def test_serializer_should_contains_expected_fields(self):
        expected = set(['description', 'source', 'details', 'events', 'date', 'level', 'env', 'arquivado'])
        self.assertEqual(expected, set(self.data.keys()))

    def test_source_field_content(self):
        self.assertEqual(self.obj.source, self.data['source'])

    def test_details_field_content(self):
        self.assertEqual(self.obj.details, self.data['details'])

    def test_events_field_content(self):
        self.assertEqual(self.obj.events, self.data['events'])

    def test_source_field_content(self):
        self.assertEqual(self.obj.source, self.data['source'])

    def test_date_field_is_serialized(self):
        self.assertIsInstance(self.data['date'], str)

    def test_level_field_content(self):
        self.assertEqual(self.obj.level, self.data['level'])

    def test_level_must_be_in_choices(self):
        self.data['level'] = 'INVALID_LEVEL'
        serializer = ErrorLogSerializer(instance=self.obj, data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['level']))

    def test_env_field_content(self):
        self.assertEqual(self.obj.env, self.data['env'])
    
    def test_env_must_be_in_choices(self):
        self.data['env'] = 'INVALID_ENV'
        serializer = ErrorLogSerializer(instance=self.obj, data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['env']))

    def test_arquivado_field_content(self):
        self.assertEqual(self.obj.arquivado, self.data['arquivado'])