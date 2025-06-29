from django.core.management.base import BaseCommand

from users.models import Payment, User
from lms.models import Course, Lesson


class Command(BaseCommand):
    help = 'Fill Payment table with test data'

    def handle(self, *args, **options):
        users = User.objects.all()
        courses = Course.objects.all()
        lessons = Lesson.objects.all()

        if not users or not courses or not lessons:
            self.stdout.write(self.style.ERROR('Необходимо сначала создать пользователей, курсы и уроки'))
            return

        payments_data = [
            {
                'user_id': 1,
                'course_id': 2,
                'lesson_id': None,
                'amount': 90000,
                'payment_method': 'cash',
                'payment_date': '2023-11-21T15:30:00Z'
            },
            {
                'user_id': 2,
                'course_id': 2,
                'lesson_id': None,
                'amount': 90000,
                'payment_method': 'transfer',
                'payment_date': '2023-11-21T17:30:00Z'
            },
            {
                'user_id': 3,
                'course_id': None,
                'lesson_id': 3,
                'amount': 3000,
                'payment_method': 'cash',
                'payment_date': '2023-11-20T11:30:00Z'
            },
            {
                'user_id': 4,
                'course_id': None,
                'lesson_id': 1,
                'amount': 6000,
                'payment_method': 'transfer',
                'payment_date': '2023-10-21T10:50:00Z'
            },
            {
                'user_id': 4,
                'course_id': 3,
                'lesson_id': None,
                'amount': 70000,
                'payment_method': 'cash',
                'payment_date': '2023-11-28T19:30:00Z'
            },
            {
                'user_id': 4,
                'course_id': 1,
                'lesson_id': None,
                'amount': 120000,
                'payment_method': 'transfer',
                'payment_date': '2023-11-03T16:00:00Z'
            },
        ]

        created_count = 0
        for data in payments_data:
            Payment.objects.create(**data)
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Успешно создано {created_count} платежей'))
