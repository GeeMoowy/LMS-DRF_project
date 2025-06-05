from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import User, Payment
from users.permissions import IsOwnerOrReadOnly
from users.serializers import UserSerializer, PaymentSerializer, UserProfileSerializer, UserProfileUpdateSerializer, \
    PublicProfileSerializer


class UserViewSet(ModelViewSet):
    """Контроллер для пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """Метод для определения прав доступа пользователя в зависимости от выбранного действия"""
        if self.action == "create":
            permission_classes = [AllowAny]  #Разрешаем создавать пользователя без аутентификации
        else:
            permission_classes = [IsAuthenticated]  # Для всех остальных действий нужна аутентификация
        return [permission() for permission in permission_classes]


class PaymentViewSet(ModelViewSet):
    """Контроллер для платежа"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = [
        'course',  # Фильтр по ID курса (/payments/?course=1)
        'lesson',  # Фильтр по ID урока (/payments/?lesson=5)
        'payment_method'  # Фильтр по способу оплаты (/payments/?payment_method=transfer)
    ]
    ordering_fields = ['payment_date']  # Сортировка по дате (/payments/?ordering=payment_date)
    ordering = ['-payment_date']  # Сортировка по умолчанию (новые сначала)


class UserProfileViewSet(ModelViewSet):
    """Контроллер для профиля пользователя"""
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        """Выбираем сериализатор в зависимости от действия и владельца"""
        if self.action in ['update', 'partial_update']:
            return UserProfileUpdateSerializer
        elif self.action in ['retrieve', 'list']:
            if self.request.user.pk == self.kwargs.get('pk', None):
                return UserProfileSerializer
            return PublicProfileSerializer
        return UserProfileSerializer  # fallback

    def get_queryset(self):
        """Оптимизация запросов"""
        queryset = super().get_queryset()
        if self.action == 'list':
            # Для списка возвращаем только публичные данные через сериализатор
            return queryset
        return queryset
