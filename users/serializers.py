from rest_framework import serializers

from users.models import User, Payment


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для получения пользователя (User).
    ***
    Создаем поле
    password: - обязательное поле только для записи.
    ***
    Включает отображение основных данных пользователя в полях:
    [id, email, avatar, phone_number, city]"""

    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'avatar', 'phone_number', 'city']

    def create(self, validated_data):
        """Создаем нового пользователя с хэшированием пароля"""
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            avatar=validated_data.get('avatar'),
            phone_number=validated_data.get('phone_number'),
            city=validated_data.get('city')
        )
        return user


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для получения платежа (Payment).
    Включает основные данные платежа. Отображает все поля."""
    class Meta:
        model = Payment
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для получения профиля пользователя."""
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'avatar', 'phone_number', 'city', 'date_joined', 'payments']
        # Добавляем поля только для чтения, для защиты от случайных изменений в этих полях
        read_only_fields = ['id', 'email', 'date_joined']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления профиля пользователя"""
    class Meta:
        model = User
        fields = ['avatar', 'phone_number', 'city']
        # Добавляем аргументы для возможности частичного обновления полей профиля пользователя
        extra_kwargs = {
            'avatar': {'required': False},
            'phone_number': {'required': False},
            'city': {'required': False}
        }
