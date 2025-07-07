from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    """Тестирование CRUD операций для уроков (Lesson)"""

    def setUp(self):
        """Настройка тестовых данных перед каждым тестом"""
        self.user = User.objects.create_user(email='test_user@sky.pro', password='testpass')
        self.course = Course.objects.create(title='Тестовый курс', description='Описание курса', owner=self.user)
        self.lesson = Lesson.objects.create(title='Тестовый урок', description='Описание урока', course=self.course,
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Тест получения деталей урока (retrieve)"""

        url = reverse('lms:lessons_retrieve', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), self.lesson.title
        )

    def test_lesson_create(self):
        """Тест создания урока (create)"""

        url = reverse('lms:lessons_create')
        data = {
            "title": "Созданный урок",
            "course": self.course.id
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertTrue(
            Lesson.objects.filter(title="Созданный урок").exists()
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        """Тест обновления урока (update)"""

        url = reverse('lms:lessons_update', args=(self.lesson.pk,))
        data = {
            "title": "Обновленный урок"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), "Обновленный урок"
        )

    def test_lesson_delete(self):
        """Тест удаления урока (delete)"""

        url = reverse('lms:lessons_destroy', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        """Тест получения списка уроков (list)"""

        url = reverse('lms:lessons_list')
        response = self.client.get(url)
        data = response.json()
        expected_result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.lesson.pk,
                    'title': self.lesson.title,
                    'description': self.lesson.description,
                    'preview': None,
                    'video_url': self.lesson.video_url,
                    'course': self.course.pk,
                    'owner': self.user.pk,
                    'price': 0,
                }
            ]
        }
        self.assertEqual(data, expected_result)


class SubscriptionTestCase(APITestCase):
    """Тестирование функционала подписок на курсы"""

    def setUp(self):
        """Настройка тестовых данных перед каждым тестом"""

        self.user = User.objects.create_user(
            email='user@sky.pro',
            password='123test'
        )
        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Описание курса',
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        """Тест создания подписки на курс"""

        url = reverse('lms:subscriptions')
        response = self.client.post(
            url, {'course_id': self.course.id}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_subscription_delete(self):
        """Тест удаления подписки на курс (отписки)"""

        # Сначала создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)

        url = reverse('lms:subscriptions')
        response = self.client.post(
            url, {'course_id': self.course.id}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
