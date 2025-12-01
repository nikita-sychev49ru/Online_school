from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from studies.models import Course, Lesson
from users.models import User


class LessonAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="email_us@email.com")
        self.course = Course.objects.create(title="Test-course", owner=self.user)
        self.lesson = Lesson.objects.create(title="Test-lesson", order="1", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('studies:lesson', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        url = reverse('studies:lesson_create')
        data = {"title": "Test-lesson2", "order": "2", "course": self.course.pk, "owner": self.user.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_create_not_valid(self):
        url = reverse('studies:lesson_create')
        data = {
            "title": "https://www.kinopoisk.ru/film/843300/",
            "order": "2",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lesson.objects.all().count(), 1)

    def test_lesson_update(self):
        url = reverse('studies:lesson_update', args=(self.lesson.pk,))
        data = {"title": "Test-lesson2"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Lesson.objects.get(title="Test-lesson2"))

    def test_lesson_delete(self):
        url = reverse('studies:lesson_delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_lesson_list(self):
        url = reverse('studies:lessons')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['results'][0]['title'], 'Test-lesson')


class CourseAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="email_us@email.com")
        self.course = Course.objects.create(title="Test-course", owner=self.user)
        self.lesson = Lesson.objects.create(title="Test-lesson", order="1", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse('studies:courses-detail', args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.course.title)

    def test_course_list(self):
        url = reverse('studies:courses-list')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['results'][0]['title'], 'Test-course')

    def test_course_create(self):
        url = reverse('studies:courses-list')
        data = {"title": "Test-course2"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_create_not_valid(self):
        url = reverse('studies:courses-list')
        data = {"title": "https://www.kinopoisk.ru/film/843300/"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Course.objects.all().count(), 1)

    @patch('studies.tasks.send_course_update_email.delay')
    def test_course_update(self, mock_send_email):
        url = reverse('studies:courses-detail', args=(self.course.pk,))
        data = {"title": "Test-course2"}
        response = self.client.patch(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get("title"), "Test-course2")

        # Проверяем, что задача была вызвана
        mock_send_email.assert_called_once_with(self.course.pk)

    def test_course_delete(self):
        url = reverse('studies:courses-detail', args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)


class SubscribeAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="email_us@email.com")
        self.course = Course.objects.create(title="Test-course", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe_create(self):
        url = reverse('studies:subscribe')
        data = {"course": self.course.pk}
        response = self.client.post(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get("message"), "подписка добавлена")
        response = self.client.post(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get("message"), "подписка удалена")
