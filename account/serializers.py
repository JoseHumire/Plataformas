"""
Account serializers
"""
from rest_framework import serializers

from django.contrib.auth.password_validation import validate_password

from account.models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
    Register serializer
    """

    password1 = serializers.CharField()
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'email', 'first_name', 'last_name',
            'password1', 'password2',
        )

    def validate(self, attrs):
        super(RegisterSerializer, self).validate(attrs)
        password1 = attrs['password1']
        password2 = attrs['password2']
        if password1 != password2:
            raise serializers.ValidationError(
                {'password1': 'Las contraseñas no coinciden'}
            )
        else:
            validate_password(attrs['password1'])

        return attrs

    def save(self, **kwargs):
        email = self.validated_data['email']
        password = self.validated_data['password1']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']

        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.is_active = False
        user.save()

        return user
