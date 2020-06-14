from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext as _

from rest_framework import serializers

from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings


User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class CustomJWTSerializer(JSONWebTokenSerializer):
    username_field = 'email'

    def validate(self, attrs):
        password = attrs.get("password")
        user_obj = User.objects.filter(email=attrs.get("email")).first() 
        if user_obj is not None:
            credentials = {
                'username':user_obj.username,
                'password': password
            }
            if all(credentials.values()):
                user = authenticate(**credentials)
                if user:
                    if not user.is_active:
                        msg = _('User account is disabled.')
                        raise serializers.ValidationError(msg)

                    payload = jwt_payload_handler(user)

                    return {
                        'token': jwt_encode_handler(payload),
                        'user': user
                    }
                else:
                    msg = _('Unable to log in with provided credentials.')
                    raise serializers.ValidationError(msg)
            else:
                msg = _('Must include "{username_field}" and "password".')
                msg = msg.format(username_field=self.username_field)
                raise serializers.ValidationError(msg)
        else:
            msg = _('Account with this email/username does not exists')
            raise serializers.ValidationError(msg)


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        queryset = User.objects.filter(email__iexact=value)
        if queryset.exists():
            raise serializers.ValidationError('User with this email already exists')
        return value

    def validate_username(self, value):
        queryset = User.objects.filter(username__iexact=value)
        if queryset.exists():
            raise serializers.ValidationError('User with this username already exists')
        return value

    def validate(self, data):
        _password = data.get('password')
        _password2 = data.get('password2')
        if _password != _password2:
            raise serializers.ValidationError('Passwords must match')
        return data

    def create(self, validated_data):
        user_obj = User(username=validated_data.get('username'), 
                        email=validated_data.get('email'))
        user_obj.set_password(validated_data.get('password'))
        user_obj.save()
        return user_obj
