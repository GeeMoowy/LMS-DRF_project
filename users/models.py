from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson


class User(AbstractUser):
    """Создание модели пользователь"""
    username = None
    email = models.EmailField(unique=True,
                              verbose_name='Email',
                              help_text='Укажите почту')
    avatar = models.ImageField(upload_to='users/avatars/',
                               verbose_name='Фото',
                               null=True,
                               blank=True,
                               help_text='Укажите аватар')
    phone_number = models.CharField(max_length=35,
                                    verbose_name='Телефон',
                                    null=True, blank=True,
                                    help_text='Укажите номер телефона')
    city = models.CharField(max_length=100,
                            verbose_name='Город',
                            null=True,
                            blank=True,
                            help_text='Укажите город')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'Пользователь {self.email}'


class Payment(models.Model):
    """Создание модели платежи"""

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='payments',
                             help_text='Выберите пользователя, к которому относится платёж')
    payment_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name='Дата оплаты')
    course = models.ForeignKey(Course,
                               on_delete=models.SET_NULL,
                               verbose_name='Оплаченный курс',
                               null=True,
                               blank=True)
    lesson = models.ForeignKey(Lesson,
                               on_delete=models.SET_NULL,
                               verbose_name='Оплаченный урок',
                               null=True,
                               blank=True)
    amount = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=20,
                                      choices=PAYMENT_METHOD_CHOICES,
                                      verbose_name='Способ оплаты')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f'Платеж {self.user.email} на сумму {self.amount}'
