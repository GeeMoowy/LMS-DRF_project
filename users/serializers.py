from rest_framework import serializers

from users.models import User, Payment


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя"""
    class Meta:
        model = User
        fields = ['id', 'email', 'avatar', 'phone_number', 'city']


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели платежей"""
    class Meta:
        model = Payment
        fields = '__all__'
