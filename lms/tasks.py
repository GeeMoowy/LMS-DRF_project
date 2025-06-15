from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from lms.models import Course, Subscription


@shared_task
def send_mail_about_update(course_id):
    """"""

    # Получаем курс по его id
    course = Course.objects.get(id=course_id)
    subscriptions = Subscription.objects.filter(course=course)
    for subscription in subscriptions:
        send_mail('Новое обновление', f'Вышло обновление курса {course.title}.',
                  EMAIL_HOST_USER, [subscription.user.email])
