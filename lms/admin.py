from django.contrib import admin

from lms.models import Course, Lesson


class CourseAdmin(admin.ModelAdmin):
    """Класс для отображения информации о курсах (Course) в админке.
    Отображает поля 'title', 'description' и 'id'. Фильтрует по полю 'title' и организован поиск по полям
    'title' и 'description'"""
    list_display = ('title', 'description', 'id')  # Поля в списке
    list_filter = ('title',)  # Фильтры справа
    search_fields = ('title', 'description')


class LessonAdmin(admin.ModelAdmin):
    """Класс для отображения информации об уроках (Lesson) в админке.
    Отображает поля 'title', 'description', 'course', 'preview' и 'video_url'. Фильтрует по полю 'title'
    и организован поиск по полям 'title' и 'description'"""
    list_display = ('title', 'description', 'course', 'preview', 'video_url')
    list_filter = ('title',)
    search_fields = ('title', 'description')


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
