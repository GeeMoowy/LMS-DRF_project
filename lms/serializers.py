from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson, Subscription
from lms.validators import ExternalLinksValidator


class LessonSerializer(ModelSerializer):
    """Сериализатор для получения урока (Lesson).
    Включает основные данные урока. Отображает все поля. Поле 'owner' отображается только для чтения.
    Есть валидация по полю 'description', для запрета использования сторонних ссылок, кроме 'youtube'"""

    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ('owner',)
        validators = [ExternalLinksValidator(field='description')]


class CourseSerializer(ModelSerializer):
    """Сериализатор для получения обучающего курса (Course).
    Включает основные данные обучающего курса, включая поля:
        - lessons_count: поле показывает количество уроков курса (вычисляемое поле)
        - lessons: поле для отображения списка уроков курса (вложенный сериализатор)
    Есть валидация по полю 'description', для запрета использования сторонних ссылок, кроме 'youtube'"""

    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'price', 'lessons_count', 'lessons', 'is_subscribed']
        read_only_fields = ('owner',)
        validators = [ExternalLinksValidator(field='description')]

    def get_lessons_count(self, obj):
        """Вычисляет общее количество уроков, связанных с курсом.
        Использует аргумент obj (Course): Объект курса, для которого рассчитывается количество уроков
        и related_name='lessons' из модели Lesson.course
        """
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """Сериализатор проверяет, подписан ли текущий пользователь на курс"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user,
                course=obj
            ).exists()
        return False
