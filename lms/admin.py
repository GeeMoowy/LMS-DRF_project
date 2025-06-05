from django.contrib import admin

from lms.models import Course, Lesson


class CourseAdmin(admin.ModelAdmin):
    """Класс для отображения информации о курсах (Course) в админке.
    Отображает поля 'title', 'owner', 'description' и 'id'. Фильтрует по полю 'owner' и организован поиск по полям
    'title' и 'description'"""
    list_display = ('title', 'owner', 'description', 'id')
    list_filter = ('owner',)
    search_fields = ('title', 'description')

    def save_model(self, request, obj, form, change):
        """Переопределяет стандартное сохранение модели в админке.
        Автоматически устанавливает владельца курса (owner) при создании нового объекта."""
        if not obj.pk:  # Только при создании
            obj.owner = request.user
        super().save_model(request, obj, form, change)


class LessonAdmin(admin.ModelAdmin):
    """Класс для отображения информации об уроках (Lesson) в админке.
    Отображает поля 'title', 'owner', 'description', 'course', 'preview' и 'video_url'. Фильтрует по полю 'owner'
    и организован поиск по полям 'title' и 'description'"""
    list_display = ('title', 'owner', 'description', 'course', 'preview', 'video_url')
    list_filter = ('owner',)
    search_fields = ('title', 'description')


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
