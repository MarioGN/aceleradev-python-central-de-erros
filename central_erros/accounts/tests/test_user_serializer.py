from django.test import TestCase
from django.contrib.auth import get_user_model

from central_erros.accounts.serializers import UserSerializer


User = get_user_model()


class DetailsErrorLogSerializerTestCase(TestCase):
    def setUp(self):
        user_data = {'username': 'apiuser', 'email': 'apiuser@email.com', 'password': 'passjwt01'}
        user = User.objects.create_user(**user_data)
        self.data = UserSerializer(instance=user).data

    def test_serializer_should_contains_expected_fields(self):
        expected = set(['username', 'email'])
        self.assertEqual(expected, set(self.data.keys()))
