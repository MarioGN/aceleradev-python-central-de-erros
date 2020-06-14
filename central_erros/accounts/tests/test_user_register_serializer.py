from django.test import TestCase
from django.contrib.auth import get_user_model

from central_erros.accounts.serializers import UserRegisterSerializer


User = get_user_model()


class UserRegisterSerializerTestCase(TestCase):
    def setUp(self):
        self.data = {
            'username': 'apiuser', 
            'email': 'apiuser@email.com', 
            'password': 'passjwt01',
            'password2': 'passjwt01'
        }

    def test_serializer_is_valid(self):
        serializer = UserRegisterSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())        

    def test_serializer_valid_email_empty(self):
        data = self.data.pop('email')
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_valid_username_empty(self):
        data = self.data.pop('username')
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_valid_password_empty(self):
        data = self.data.pop('password')
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_valid_password2_empty(self):
        data = self.data.pop('password2')
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
