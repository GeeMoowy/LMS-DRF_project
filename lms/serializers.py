from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    """Сериализатор для получения урока (Lesson).
    Включает основные данные урока. Отображает все поля. Поле 'owner' отображается только для чтения"""

    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ('owner',)


class CourseSerializer(ModelSerializer):
    """Сериализатор для получения обучающего курса (Course).
    Включает основные данные обучающего курса, включая поля:
        - lessons_count: поле показывает количество уроков курса (вычисляемое поле)
        - lessons: поле для отображения списка уроков курса (вложенный сериализатор)"""

    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'lessons_count', 'lessons']
        read_only_fields = ('owner',)

    def get_lessons_count(self, obj):
        """Вычисляет общее количество уроков, связанных с курсом.
        Использует аргумент obj (Course): Объект курса, для которого рассчитывается количество уроков
        и related_name='lessons' из модели Lesson.course
        """
        return obj.lessons.count()
