from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

from users.models import User, Payment
from users.serializers import UserProfileSerializer, PaymentSerializer


class UserViewSet(ModelViewSet):
    """Контроллер для пользователя"""
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer


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
