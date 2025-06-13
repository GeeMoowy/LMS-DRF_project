from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson
from users.models import User, Payment
from users.permissions import IsOwnerOrReadOnly
from users.serializers import UserSerializer, PaymentSerializer, UserProfileSerializer, UserProfileUpdateSerializer, \
    PublicProfileSerializer
from users.services import create_stripe_sessions, create_stripe_price, create_stripe_product


class UserViewSet(ModelViewSet):
    """Контроллер для пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """Метод для определения прав доступа пользователя в зависимости от выбранного действия"""
        if self.action == "create":
            permission_classes = [AllowAny]  # Разрешаем создавать пользователя без аутентификации
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


class PaymentCreateAPIView(CreateAPIView):
    """API endpoint для создания платежной сессии через Stripe.

    Позволяет создавать платежи как для курсов, так и для отдельных уроков.
    При создании платежа:
    1. Валидирует входные данные
    2. Создает продукт в Stripe
    3. Создает цену в Stripe (с конвертацией рублей в копейки)
    4. Создает сессию оплаты в Stripe
    5. Сохраняет платеж в базу данных

    Требуемые параметры в URL:
    - Для курса: /payments/course/<int:course_id>/
    - Для урока: /payments/lesson/<int:lesson_id>/

    Возвращает:
    - 201 Created: при успешном создании (с URL для оплаты)
    - 400 Bad Request: при ошибках валидации
    - 404 Not Found: если курс/урок не существует"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        """Обрабатывает POST-запрос для создания платежа.
        Возвращает:
        - Response: JSON с payment_url или сообщением об ошибке
        Логика работы:
        1. Определяет тип оплачиваемого объекта (курс/урок)
        2. Получает объект и его цену
        3. Подготавливает данные для платежа
        4. Валидирует данные через сериализатор
        5. Создает платежную сессию
        6. Возвращает URL для оплаты"""

        obj_type, obj_id = self.get_object_type(kwargs)  # Определяем тип объекта (курс или урок)
        obj, amount = self.get_payment_object(obj_type, obj_id)  # Получаем объект и его цену

        if not obj:
            return Response(
                {'error': 'Необходимо указать ID курса или урока'},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment_data = self.prepare_payment_data(request.user, obj, obj_type, amount)  # Готовим данные для платежа

        serializer = self.get_serializer(data=payment_data)  # Создаем сериализатор и валидируем данные
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer, obj, obj_type)  # Создаем платеж в Stripe и сохраняем в БД

        return Response(
            {'payment_url': serializer.data['link']},
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer.data)
        )

    def get_object_type(self, kwargs):
        """Определяет тип оплачиваемого объекта по параметрам URL.
        Возвращает:
        - tuple: (тип_объекта, id_объекта) или (None, None)
        Возможные типы:
        - 'course': если передан course_id
        - 'lesson': если передан lesson_id"""

        if 'course_id' in kwargs:
            return 'course', kwargs['course_id']
        elif 'lesson_id' in kwargs:
            return 'lesson', kwargs['lesson_id']
        return None, None

    def get_payment_object(self, obj_type, obj_id):
        """Получает объект оплаты (курс или урок) по ID.
        Возвращает: tuple: (объект, цена) или (None, None)
        Вызывает: 404 Not Found: если объект не существует"""

        if not obj_type or not obj_id:
            return None, None

        if obj_type == 'course':
            obj = get_object_or_404(Course, id=obj_id)
            return obj, obj.price
        else:
            obj = get_object_or_404(Lesson, id=obj_id)
            return obj, obj.price

    def prepare_payment_data(self, user, obj, obj_type, amount):
        """Подготавливает данные для создания платежа.
        Возвращает: dict: словарь с данными для платежа:
            {'user': id пользователя,
            'amount': сумма,
            'payment_method': способ оплаты,
            'course' или 'lesson': id объекта}"""

        data = {
            'user': user.id,
            'amount': amount,
            'payment_method': 'transfer',
        }
        if obj_type == 'course':
            data['course'] = obj.id
        else:
            data['lesson'] = obj.id
        return data

    def perform_create(self, serializer, obj, obj_type):
        """Основная логика создания платежа.
        Выполняет:
        1. Создание продукта в Stripe
        2. Создание цены в Stripe
        3. Создание платежной сессии
        4. Сохранение платежа в БД"""

        product_name = f"Курс: {obj.title}" if obj_type == 'course' else f"Урок: {obj.title}"
        product_data = {
            "name": product_name,
            "description": obj.description if hasattr(obj, 'description') else product_name
        }
        stripe_product = create_stripe_product(product_data)
        stripe_price = create_stripe_price(obj.price, stripe_product)
        session_id, payment_url = create_stripe_sessions(stripe_price)

        serializer.save(
            user=self.request.user,
            session_id=session_id,
            link=payment_url,
            amount=obj.price
        )
