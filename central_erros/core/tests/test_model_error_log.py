from datetime import datetime
from django.test import TestCase
from django.core.validators import ValidationError

from central_erros.core.models import ErrorLog


class ErrorLogModelTestCase(TestCase):
    def setUp(self):
        self.obj = ErrorLog.objects.create(
            source='127.0.0.1',
            description='acceleration.Detail: <not found>',
            details='File "/app/source/core/service.py", line 182, in (*App).Error',
            raised_at=datetime.now()
        )

    def test_error_log_created_should_exists(self):
        self.assertTrue(ErrorLog.objects.exists())
    
    def get_meta_field(self, field):
        """ Recupera o field do modelo pelo nome. """
        return ErrorLog._meta.get_field(field)
    
    def test_source_cant_be_blank(self):
        self.assertFalse(self.get_meta_field('source').blank)

    def test_description_cant_be_blank(self):
        self.assertFalse(self.get_meta_field('description').blank)

    def test_details_cant_be_blank(self):
        self.assertFalse(self.get_meta_field('details').blank)

    def test_events_cant_be_blank(self):
        self.assertFalse(self.get_meta_field('details').blank)

    def test_events_cant_be_null(self):
        self.assertFalse(self.get_meta_field('details').null)

    def test_events_default_to_1(self):
        self.assertEqual(self.get_meta_field('events').default, 1)

    def test_events_cant_be_less_than_1(self):
        invalid_obj = self.obj
        invalid_obj.events = 0

        with self.assertRaises(ValidationError):
            invalid_obj.full_clean()

    def test_raised_at_cant_be_blank(self):
        self.assertFalse(self.get_meta_field('raised_at').null)

    def test_raised_at_cant_be_null(self):
        self.assertFalse(self.get_meta_field('raised_at').null)

    def test_create_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_updated_at(self):
        self.assertIsInstance(self.obj.updated_at, datetime)
