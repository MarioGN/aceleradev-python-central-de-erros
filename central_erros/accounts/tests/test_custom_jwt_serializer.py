from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.serializers import ValidationError

from central_erros.accounts.serializers import CustomJWTSerializer


User = get_user_model()


class CustomJWTSerializerTestcase(TestCase):
    def setUp(self):
        user_data = {'username': 'apiuser', 'email': 'apiuser@email.com', 'password': 'passjwt01'}
        user = User.objects.create_user(**user_data)       

    def test_serializer_is_valid(self):
        data = {'email': 'apiuser@email.com', 'password': 'passjwt01'}
        serializer = CustomJWTSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_with_invalid_email_should_raise_ValidationError(self):
        data = {'email': 'invalidemail@email.com', 'password': 'passjwt01'}
        serializer = CustomJWTSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.validate(data)

    def test_serializer_with_invalid_password_should_raise_ValidationError(self):
        data = {'email': 'apiuser@email.com', 'password': 'invalidpass'}
        serializer = CustomJWTSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.validate(data)

    def test_serializer_without_email_should_raise_ValidationError(self):
        data = {'password': 'passjwt01'}
        serializer = CustomJWTSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.validate(data)

    def test_serializer_without_password_should_raise_ValidationError(self):
        data = {'email': 'apiuser@email.com'}
        serializer = CustomJWTSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.validate(data)
