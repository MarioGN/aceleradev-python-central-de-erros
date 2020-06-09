from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from central_erros.api.models import ErrorLog


VALID_PAYLOAD = {
    "description": "acceleration.Detail: <not found>",   
    "source": "127.0.0.1",
    "details": "File \"/app/source/core/service.py\", line 182, in (*App).Error",
    "events": "10",
    "date": "2020-06-04T13:41:28+00:00",
    "level": "ERROR",
    "env": "DEV",
    "arquivado": "False"
}


class ListCreateLogsAPIView(TestCase):
    def setUp(self):
        client = APIClient()
        url = reverse('api:list-create-logs')
        self.response = client.post(url, VALID_PAYLOAD)

    def test_post_create_should_return_status_201(self):
        self.assertEqual(status.HTTP_201_CREATED, self.response.status_code)

    def test_post_create_should_persist_new_log(self):
        self.assertEqual(len(ErrorLog.objects.all()), 1)


class ListCreateLogsAPIViewInvalid(TestCase):
    def setUp(self):
        self.payload = VALID_PAYLOAD
        self.url = reverse('api:list-create-logs')
        self.client = APIClient()

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
            ('details', 'Missing the details field'),
            ('date', 'Missing the date field'),
            ('level', 'Missing the level field'),
            ('env', 'Missing the env field'),
        )

        for field_name, subtest_description in missing_fields:
            with self.subTest(subtest_description):
                data = self.payload.copy()
                data.pop(field_name)
                response = self._post_request(data)
                
                self.assertIn("required", response.data[field_name][0].code)