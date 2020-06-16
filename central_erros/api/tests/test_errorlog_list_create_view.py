from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from central_erros.api.models import ErrorLog
from central_erros.api.serializers import ErrorLogSerializer
from .utils import JWTAuthenticatedTestCase


User = get_user_model()


VALID_PAYLOAD = {
    "description": "acceleration.Detail: <not found>",   
    "source": "127.0.0.1",
    "details": "File \"/app/source/core/service.py\", line 182, in (*App).Error",
    "events": "10",
    "date": "2020-06-04T13:41:28+00:00",
    "level": "ERROR",
    "env": "DEV",
}


class FilterENVGETListCreateLogsAPIView(JWTAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self._make_logs(quantity=3)
        self._make_logs(quantity=2, env='HOMOLOGATION')
        self._make_logs(quantity=5, env='PRODUCTION')

    def test_get_simple_env_filter_should_return_status_200(self):
        response = self.client.get('/v1/api/logs/', {'env': 'dev'}, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_filter_errorlog_by_env_DEV_should_return_3_logs(self):
        response = self.client.get('/v1/api/logs/', {'env': 'dev'}, format='json')
        self.assertEqual(3, response.data['count'])
        
    def test_get_filter_errorlog_by_env_HOMOLOGACAO_should_return_2_logs(self):
        response = self.client.get('/v1/api/logs/', {'env': 'homologation'}, format='json')
        self.assertEqual(2, response.data['count'])

    def test_get_filter_errorlog_by_env_produção_should_return_5_logs(self):
        response = self.client.get('/v1/api/logs/', {'env': 'production'}, format='json')
        self.assertEqual(5, response.data['count'])


class OrderByFieldGETListCreateLogsAPIView(JWTAuthenticatedTestCase):
    def setUp(self):
        super().setUp()

    def test_ordering_errorlogs_by_events_field(self):
        events_list = [43, 89, 290]
        for evs in events_list:
            self._make_logs(events=evs)
        response = self.client.get('/v1/api/logs/', {'ordering': 'events'}, format='json')
        response_events = [int(log['events']) for log in response.data['results']]
        self.assertSequenceEqual(events_list, response_events)

    def test_ordering_errorlogs_by_events_field_descending(self):
        events_list = [43, 89, 290]
        for evs in events_list:
            self._make_logs(events=evs)
        response = self.client.get('/v1/api/logs/', {'ordering': '-events'}, format='json')
        response_events = [int(log['events']) for log in response.data['results']]
        response_events.reverse()
        self.assertSequenceEqual(events_list, response_events)

    def test_ordering_errorlogs_by_level_field(self):
        level_list = ['CRITICAL', 'DEBUG', 'ERROR', 'INFO', 'WARNING']
        for lvl in level_list:
            self._make_logs(level=lvl)
        response = self.client.get('/v1/api/logs/', {'ordering': 'level'}, format='json')
        response_levels = [log['level'] for log in response.data['results']]
        self.assertSequenceEqual(level_list, response_levels)

    def test_ordering_errorlogs_by_level_field_descending(self):
        level_list = ['CRITICAL', 'DEBUG', 'ERROR', 'INFO', 'WARNING']
        for lvl in level_list:
            self._make_logs(level=lvl)
        response = self.client.get('/v1/api/logs/', {'ordering': '-level'}, format='json')
        response_levels = [log['level'] for log in response.data['results']]
        level_list.reverse()
        self.assertSequenceEqual(level_list, response_levels)


class SearchFieldGETListCreateLogsAPIView(JWTAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self._make_logs(quantity=2)
        self._make_logs(quantity=1, level='INFO')
        self._make_logs(quantity=5, level='WARNING')
        self._make_logs(quantity=3, level='DEBUG', description='INFO LOG')
        self._make_logs(quantity=1, level='CRITICAL', description='CRITICAL ERROR', source='149.10.145.90')

    def test_get_field_filter_should_return_status_200(self):
        response = self.client.get('/v1/api/logs/', {'field': 'level', 'search': 'ERROR'}, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_filter_errorlog_by_level_ERROR_should_return_2_logs(self):
        response = self.client.get('/v1/api/logs/', {'field': 'level', 'search': 'ERROR'}, format='json')
        self.assertEqual(2, response.data['count'])

    def test_get_filter_errorlog_by_level_INFO_should_return_1_log(self):
        response = self.client.get('/v1/api/logs/', {'field': 'level', 'search': 'INFO'}, format='json')
        self.assertEqual(1, response.data['count'])

    def test_get_filter_errorlog_by_level_WARNING_should_return_5_logs(self):
        response = self.client.get('/v1/api/logs/', {'field': 'level', 'search': 'WARNING'}, format='json')
        self.assertEqual(5, response.data['count'])
        
    def test_get_filter_errorlog_by_description_should_return_8_log(self):
        response = self.client.get('/v1/api/logs/', {'field': 'description', 'search': 'descript'}, format='json')
        self.assertEqual(8, response.data['count'])

    def test_get_filter_errorlog_by_description_should_return_3_log(self):
        response = self.client.get('/v1/api/logs/', {'field': 'description', 'search': 'INFO'}, format='json')
        self.assertEqual(3, response.data['count'])

    def test_get_filter_errorlog_by_source_should_return_11_logs(self):
        response = self.client.get('/v1/api/logs/', {'field': 'source', 'search': '127.0.0.1'}, format='json')
        self.assertEqual(11, response.data['count'])

    def test_get_filter_errorlog_by_source_should_return_1_log(self):
        response = self.client.get('/v1/api/logs/', {'field': 'source', 'search': '149.10.145.90'}, format='json')
        self.assertEqual(1, response.data['count'])


class GETListCreateLogsAPIView(JWTAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        user = User.objects.all().first()
        ErrorLog.objects.create(user=user, **VALID_PAYLOAD)
        url = reverse('api:list-create-logs')
        self.response = self.client.get(url, format='json')

    def test_get_should_return_status_200(self):
        self.assertEqual(status.HTTP_200_OK, self.response.status_code)

    def test_get_serialized_data(self):
        logs = ErrorLog.objects.all()
        serialized_data = ErrorLogSerializer(logs, many=True).data
        self.assertEqual(self.response.data['results'], serialized_data)


class POSTListCreateLogsAPIView(JWTAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('api:list-create-logs')
        self.response = self.client.post(self.url, VALID_PAYLOAD)

    def test_post_create_should_return_status_201(self):
        self.assertEqual(status.HTTP_201_CREATED, self.response.status_code)

    def test_post_create_should_persist_new_log(self):
        self.assertEqual(len(ErrorLog.objects.all()), 1)


class POSTInvalidListCreateLogsAPIView(JWTAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('api:list-create-logs')
        self.payload = VALID_PAYLOAD

    def _post_request(self, payload):
        return self.client.post(self.url, payload, format='json')

    def test_post_create_with_invalid_paylod_should_return_status_400(self):
        response = self._post_request({})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post_create_with_invalid_paylod_should_return_required_fields(self):
        """
        Testa a submissão de post create com campos obrigatórios faltando.
        """
        missing_fields = (
            # tupla (nome_do_campo, descricao_do_subteste)
            ('description', 'Missing the description field'),
            ('source', 'Missing the source field'),
            ('date', 'Missing the date field'),
            ('level', 'Missing the level field'),
            ('env', 'Missing the env field'),
        )

        for field_name, subtest_description in missing_fields:
            with self.subTest(subtest_description):
                data = VALID_PAYLOAD.copy()
                data.pop(field_name)
                response = self._post_request(data)
                self.assertIn("required", response.data[field_name][0].code)
