from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    """Сериализатор для модели Lesson"""
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    """Сериализатор для модели Course"""
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'lessons_count', 'lessons']

    def get_lessons_count(self, obj):
        """Метод получает количество уроков в курсе"""
        return obj.lessons.count()
