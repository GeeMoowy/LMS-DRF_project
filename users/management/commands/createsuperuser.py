from django.core.management import CommandError
from django.contrib.auth.management.commands.createsuperuser import Command as BaseCommand
from users.models import User


class Command(BaseCommand):
    """Кастомная команда для создания суперпользователя с email-авторизацией"""

    help = 'Создает суперпользователя с email вместо username'

    def add_arguments(self, parser):
        """Добавляем обязательный аргумент --email"""
        parser.add_argument(
            '--email',
            dest='email',
            required=True,
            help='Email администратора'
        )
        parser.add_argument(
            '--password',
            dest='password',
            help='Пароль (если не указан, будет запрошен)'
        )

    def handle(self, *args, **options):
        email = options['email']
        password = options.get('password')

        try:
            User.objects.create_superuser(
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'Суперпользователь {email} создан'))
        except Exception as e:
            raise CommandError(f'Ошибка: {str(e)}')
