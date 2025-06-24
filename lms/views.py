from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from lms.models import Course, Lesson, Subscription
from lms.paginations import CustomPagination
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsOwner, IsModerator
from lms.tasks import send_mail_about_update


class CourseViewSet(ModelViewSet):
    """Контроллер для работы с объектами Course (курса).
    Переопределен метод perform_create для сохранения в поле 'owner' текущего пользователя.
    Разрешен показ только курсов созданных текущим пользователем. Добавлена пагинация для вывода списка курсов"""
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        """Возвращает все курсы если пользователь в группе 'Модераторы',
        иначе возвращает только созданные пользователем курсы"""
        user = self.request.user
        if user.groups.filter(name='Модераторы'):
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def get_permissions(self):
        """Настраиваем права в зависимости от действия"""
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        else:  # list, retrieve
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        """Автоматически назначаем текущего пользователя владельцем"""
        if self.request.user.groups.filter(name='Модераторы').exists():
            raise PermissionDenied("Модераторы не могут создавать курсы")
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """При обновлении курса отправляем уведомления подписчикам."""
        instance = serializer.save()
        # Запускаем асинхронную задачу Celery для рассылки писем
        send_mail_about_update.delay(instance.id)

    def perform_destroy(self, instance):
        """Удаление с проверкой прав"""
        if not instance.owner == self.request.user:
            raise PermissionDenied("Вы не можете удалить чужой курс")
        instance.delete()


class LessonCreateApiView(CreateAPIView):
    """Контроллер для создания объекта Lesson (урок)
    с автоматическим назначением поля 'owner' текущим пользователем"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        """Автоматически назначаем текущего пользователя владельцем"""
        if self.request.user.groups.filter(name='Модераторы').exists():
            raise PermissionDenied("Модераторы не могут создавать уроки")
        serializer.save(owner=self.request.user)


class LessonListApiView(ListAPIView):
    """Просмотр списка уроков (свои для пользователей, все для модераторов).
    Добавлена пагинация для вывода списка курсов"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonRetrieveApiView(RetrieveAPIView):
    """Контроллер для просмотра деталей выбранного урока, созданного текущим пользователем"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & (IsOwner | IsModerator)]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonUpdateApiView(UpdateAPIView):
    """Контроллер для редактирования выбранного урока, созданного текущим пользователем"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & (IsOwner | IsModerator)]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonDestroyApiView(DestroyAPIView):
    """Удаление урока (только владельцы)"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Lesson.objects.filter(owner=self.request.user)


class SubscriptionAPIView(APIView):
    """Контроллер для управления подписками на обновления для пользователя"""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Метод post реализует логику управления подписками пользователей на курсы"""

        # Получаем данные текущего пользователя, id курса из тела запроса и находим курс или возвращаем 404
        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        # Пытаемся найти подписку для данного пользователя и курса или создать ее
        subscription, created = Subscription.objects.get_or_create(
            user=user,
            course=course
        )

        # Если подписка не была создана (существует), удаляем ее. Если создана, выводим сообщение о создании подписки
        if not created:
            subscription.delete()
            message = 'Подписка удалена'
        else:
            message = 'Подписка добавлена'

        return Response({"message": message}, status=status.HTTP_200_OK)
