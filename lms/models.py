from django.db import models

from config import settings


class Course(models.Model):
    """Модель обучающего курса. Хранит информацию об обучающем курсе в полях:
        - title (название): название обучающего курса
        - preview (изображение): картинка с изображением обучающего курса
        - description (описание): описание обучающего курса
        - owner (владелец): при создании автоматически заполняется текущим пользователем"""

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
    price = models.PositiveIntegerField(verbose_name='Цена курса',
                                   default=0,
                                   help_text='Введите цену курса')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.SET_NULL,
                              verbose_name='Владелец',
                              null=True,
                              blank=True,
                              related_name='courses')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока. Связана с моделью Course (обучающего курса) и хранит информацию об уроке в полях:
        - course: поле внешнего ключа для связи с моделью Course
        - title: название урока
        - description: описание урока
        - preview: картинка с изображением урока
        - video_url: ссылка на ресурс с видео-контентом урока
        - owner (владелец): при создании автоматически заполняется текущим пользователем"""

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
    price = models.PositiveIntegerField(verbose_name='Цена урока',
                                        default=0,
                                        help_text='Введите цену урока')
    preview = models.ImageField(upload_to='lms/preview/lesson/',
                                verbose_name='Картинка',
                                null=True,
                                blank=True,
                                help_text='Укажите картинку урока')
    video_url = models.URLField(verbose_name="Ссылка на видео",
                                blank=True,
                                null=True,
                                help_text="Вставьте ссылку на видео")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.SET_NULL,
                              verbose_name='Владелец',
                              null=True,
                              blank=True,
                              related_name='lessons')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title


class Subscription(models.Model):
    """Модель подписки на обновления курса для пользователя. Имеет поля:
        - user: поле внешнего ключа для связи с моделью User
        - course: поле внешнего ключа для связи с моделью Course"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='user_subscriptions',
                             verbose_name='Пользователь')
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name='course_subscriptions',
                               verbose_name='Курс')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('user', 'course')

    def __str__(self):
        return f'{self.user.email} -> {self.course.title}'
