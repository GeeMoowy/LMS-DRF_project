from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=100,
                             verbose_name='Название курса',
                             help_text='Введите название курса')
    preview = models.ImageField(upload_to='lms/preview/course/',
                               verbose_name='Картинка',
                               null=True,
                               blank=True,
                               help_text='Укажите картинку курса')
    description = models.TextField(verbose_name='Описание',
                                   null=True,
                                   blank=True,
                                   help_text='Введите описание курса')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               verbose_name='Курс',
                               related_name='lessons',
                               help_text='Выберите курс, к которому относится урок')
    title = models.CharField(max_length=100,
                             verbose_name='Название урока',
                             help_text='Введите название урока')
    description = models.TextField(verbose_name='Описание',
                                   null=True,
                                   blank=True,
                                   help_text='Введите описание урока')
    preview = models.ImageField(upload_to='lms/preview/lesson/',
                                verbose_name='Картинка',
                                null=True,
                                blank=True,
                                help_text='Укажите картинку урока')
    video_url = models.URLField(verbose_name="Ссылка на видео",
                                blank=True,
                                null=True,
                                help_text="Вставьте ссылку на видео")

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title
