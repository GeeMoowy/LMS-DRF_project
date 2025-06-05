from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsOwner, IsModerator


class CourseViewSet(ModelViewSet):
    """Контроллер для работы с объектами Course (курса).
    Переопределен метод perform_create для сохранения в поле 'owner' текущего пользователя.
    Разрешен показ только курсов созданных текущим пользователем"""
    serializer_class = CourseSerializer

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
            self.permission_classes = [IsAuthenticated, IsOwner]
        else:  # list, retrieve
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        """Автоматически назначаем текущего пользователя владельцем"""
        if self.request.user.groups.filter(name='Модераторы').exists():
            raise PermissionDenied("Модераторы не могут создавать курсы")
        serializer.save(owner=self.request.user)

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
    """Просмотр списка уроков (свои для пользователей, все для модераторов)"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonRetrieveApiView(RetrieveAPIView):
    """Контроллер для просмотра деталей выбранного урока, созданного текущим пользователем"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner, IsModerator]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonUpdateApiView(UpdateAPIView):
    """Контроллер для редактирования выбранного урока, созданного текущим пользователем"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner, IsModerator]

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
