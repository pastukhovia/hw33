import django.core.exceptions
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User


class RetrieveUpdateDeleteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UserCreateSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'password_repeat']

    def is_valid(self, *, raise_exception=False):
        if self.initial_data['password'] != self.initial_data['password_repeat']:
            raise ValidationError({"password": ["Passwords don't match"]})

        try:
            validate_password(self.initial_data['password'])
        except django.core.exceptions.ValidationError as errors:
            raise ValidationError({"password": [error for error in errors]})

        self.initial_data.pop('password_repeat')
        super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        user.set_password(validated_data['password'])

        user.save()
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    class Meta:
        model = User
        fields = ['old_password', 'new_password']

    def is_valid(self, *, raise_exception=False):
        if not self.context['request'].user.check_password(self.initial_data['old_password']):
            raise ValidationError({"old_password": ["Old password doesn't match"]})

        try:
            validate_password(self.initial_data['new_password'])
        except django.core.exceptions.ValidationError as errors:
            raise ValidationError({"new_password": [error for error in errors]})

        super().is_valid(raise_exception=raise_exception)

    def save(self):
        user = super().save()
        user.set_password(self.initial_data['new_password'])
        user.save()

        return user
