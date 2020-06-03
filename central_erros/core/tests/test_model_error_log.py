from datetime import datetime
from django.test import TestCase
from django.core.validators import ValidationError

from central_erros.core.models import ErrorLog


class ErrorLogModelTest(TestCase):
    def setUp(self):
        self.log = ErrorLog.objects.create(
            source='127.0.0.1',
            description='acceleration.Detail: <not found>',
            details='File "/app/source/core/service.py", line 182, in (*App).Error',
            raised_at=datetime.now()
        )

    def test_create(self):
        self.assertTrue(ErrorLog.objects.exists())

    def test_source_cant_be_blank(self):
        field = ErrorLog._meta.get_field('source')
        self.assertFalse(field.blank)

    def test_description_cant_be_blank(self):
        field = ErrorLog._meta.get_field('description')
        self.assertFalse(field.blank)

    def test_details_cant_be_blank(self):
        field = ErrorLog._meta.get_field('details')
        self.assertFalse(field.blank)

    def test_events_cant_be_blank(self):
        field = ErrorLog._meta.get_field('events')
        self.assertFalse(field.blank)

    def test_events_cant_be_null(self):
        field = ErrorLog._meta.get_field('events')
        self.assertFalse(field.null)

    def test_events_default_to_1(self):
        field = ErrorLog._meta.get_field('events')
        self.assertEqual(field.default, 1)

    def test_events_cant_be_less_than_1(self):
        invalid_events_log = ErrorLog.objects.create(
            source='127.0.0.1',
            description='acceleration.Detail: <not found>',
            details='File "/app/source/core/service.py", line 182, in (*App).Error',
            events=0,
            raised_at=datetime.now()
        )

        with self.assertRaises(ValidationError):
            invalid_events_log.full_clean()

    def test_raised_at(self):
        self.assertIsInstance(self.log.raised_at, datetime)

    def test_raised_at_cant_be_null(self):
        field = ErrorLog._meta.get_field('raised_at')
        self.assertFalse(field.null)

    def test_raised_at_cant_be_blank(self):
        field = ErrorLog._meta.get_field('raised_at')
        self.assertFalse(field.blank)

    def test_create_at(self):
        self.assertIsInstance(self.log.created_at, datetime)

    def test_updated_at(self):
        self.assertIsInstance(self.log.updated_at, datetime)
