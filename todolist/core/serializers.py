from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'password_repeat']

    def is_valid(self, *, raise_exception=False):
        if self.initial_data['password'] != self.initial_data['password_repeat']:
            raise ValidationError({"password": ["Passwords don't match"]})

        validate_password(self.initial_data['password'])

        self.initial_data.pop('password_repeat')
        super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        user.set_password(validated_data['password'])

        user.save()
        return user
