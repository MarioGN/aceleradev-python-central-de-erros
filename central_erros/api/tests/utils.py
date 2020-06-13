from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from central_erros.api.models import ErrorLog


User = get_user_model()


class JWTAuthenticatedTestCase(TestCase):
    """
    Cria uma instância de APIClient e configura as credentials.
    """
    def setUp(self):
        self.client = APIClient()
        self._jwt_authenticate()

    def _jwt_authenticate(self):
        user_data = {'username': 'apiuser', 'email': 'apiuser@email.com', 'password': 'passjwt01'}
        User.objects.create_user(**user_data)
        url = reverse('accounts:login')        
        response = self.client.post(url, user_data, format='json')
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

    def _make_logs(self, quantity=1, env='DEV', level='ERROR', events=1, description='description', source='127.0.0.1'):
        user = User.objects.all().first()
        for i in range(quantity):
            ErrorLog.objects.create(
                user=user,
                description=f'{description} {i}', 
                source=source,
                details=f'Error log at line {i}',
                events=events,
                date=timezone.now(),
                level=level,
                env=env,
            )
