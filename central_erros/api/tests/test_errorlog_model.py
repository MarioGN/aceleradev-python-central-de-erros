import datetime

from django.test import TestCase
from django.utils import timezone
from django.core.validators import ValidationError

from central_erros.api.models import ErrorLog


class ErrorLogModelTestCase(TestCase):
    def setUp(self):
        self.obj = ErrorLog.objects.create(
            description='acceleration.Detail: <not found>',
            source='127.0.0.1',
            details='File "/app/source/core/service.py", line 182, in (*App).Error',
            events=10,
            date=timezone.now(),
            level='ERROR',
            env='DEV',
            archived=False,
        )

    def get_meta_field(self, field):
        """ Recupera os metadados do field pelo nome. """
        return ErrorLog._meta.get_field(field)

    def test_errorlog_created_should_exists(self):
        self.assertTrue(ErrorLog.objects.exists())

    def test_description_cant_be_blank(self):
        self.assertFalse(self.get_meta_field('description').blank)

    def test_description_cant_be_null(self):
        self.assertFalse(self.get_meta_field('description').null)

    def test_description_max_length_should_be_50(self):
        self.assertEqual(self.get_meta_field('description').max_length, 256)

    def test_source_cant_be_blank(self):
        self.assertFalse(self.get_meta_field('source').blank)

    def test_source_cant_be_null(self):
        self.assertFalse(self.get_meta_field('source').null)

    def test_source_max_length_should_be_64(self):
        self.assertEqual(self.get_meta_field('source').max_length, 39)

    def test_details_cant_be_blank(self):
        self.assertFalse(self.get_meta_field('details').blank)

    def test_details_cant_be_null(self):
        self.assertFalse(self.get_meta_field('details').null)

    def test_details_max_length_should_be_None(self):
        self.assertEqual(self.get_meta_field('details').max_length, None)

    def test_events_cant_be_blank(self):
        self.assertFalse(self.get_meta_field('events').blank)

    def test_events_cant_be_null(self):
        self.assertFalse(self.get_meta_field('events').null)

    def test_events_default_to_1(self):
        self.assertEqual(self.get_meta_field('events').default, 1)

    def test_events_cant_be_less_than_1(self):
        self.obj.events = 0
        with self.assertRaises(ValidationError):
            self.obj.full_clean()

    def test_date(self):
        self.assertIsInstance(self.obj.date, datetime.datetime)

    def test_date_cant_be_blank(self):
        self.assertFalse(self.get_meta_field('date').null)

    def test_date_cant_be_null(self):
        self.assertFalse(self.get_meta_field('date').null)

    def test_level_cant_be_blank(self):
        self.assertFalse(self.get_meta_field('level').blank)

    def test_level_cant_be_null(self):
        self.assertFalse(self.get_meta_field('level').null)

    def test_level_max_length_should_be_16(self):
        self.assertEqual(self.get_meta_field('level').max_length, 16)

    def test_level_invalid_option_should_raise_value_error(self):
        with self.assertRaises(ValidationError):
            self.obj.level = 'INVALID_OPTION'
            self.obj.full_clean()

    def test_env_cant_be_blank(self):
        self.assertFalse(self.get_meta_field('env').blank)

    def test_env_cant_be_null(self):
        self.assertFalse(self.get_meta_field('env').null)

    def test_env_max_length_should_be_16(self):
        self.assertEqual(self.get_meta_field('env').max_length, 16)

    def test_env_invalid_option_should_raise_value_error(self):
        with self.assertRaises(ValidationError):
            self.obj.env = 'INVALID_OPTION'
            self.obj.full_clean()

    def test_archived(self):
        self.assertIsInstance(self.obj.archived, bool)

    def test_archived_default_to_false(self):
        self.assertFalse(self.get_meta_field('archived').default)

    def test_create_at(self):
        self.assertIsInstance(self.obj.created_at, datetime.datetime)

    def test_updated_at(self):
        self.assertIsInstance(self.obj.updated_at, datetime.datetime)

    def test_verbose_name(self):
        verbose_name = ErrorLog._meta.verbose_name
        self.assertEqual(verbose_name, 'Error Log')

    def test_verbose_name_plural(self):
        verbose_name_plural = ErrorLog._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, 'Error Logs')

    def test_errorlog_str(self):
        self.assertEqual(self.obj.description, str(self.obj))
