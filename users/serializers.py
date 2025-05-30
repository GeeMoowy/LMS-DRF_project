from rest_framework import serializers

from users.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'avatar', 'phone_number', 'city']
        extra_kwargs = {
            'email': {'read_only': True}  # Запрет на изменение email
        }
