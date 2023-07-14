from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import TgUser


class TgUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TgUser
        fields = ['user']

    def update(self, instance, validated_data):
        if instance.user_id:
            raise ValidationError(detail={'detail': 'This code already used'})

        instance.user_id = self.context['request'].user
        instance.save()

        return instance
