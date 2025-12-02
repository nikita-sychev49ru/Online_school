from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from studies.models import Course, Lesson, Subscribe
from studies.paginators import StudiesPagination
from studies.serializers import CourseSerializer, LessonSerializer, SubscribeSerializer
from users.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """вьюсет представлений для объектов модели Курс"""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = StudiesPagination

    def get(self, request):
        queryset = Course.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = CourseSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def update(self, request, *args, **kwargs):
        # для обновления курса (PUT)
        instance = self.get_object()
        response = super().update(request, *args, **kwargs)

        # отправка сообщения подписчикам об обновлении курса
        if response.status_code == status.HTTP_200_OK:
            from studies.tasks import send_course_update_email

            send_course_update_email.delay(instance.pk)
        return response

    def partial_update(self, request, *args, **kwargs):
        # для частичного обновления курса (PATCH)
        return self.update(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~IsModer,)
        elif self.action == 'destroy':
            self.permission_classes = (IsOwner,)
        elif self.action in ['retrieve', 'update']:
            self.permission_classes = (IsModer | IsOwner,)
        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    """представление для создания объекта Урок"""

    serializer_class = LessonSerializer
    permission_classes = (~IsModer,)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """представление для просмотра списка объектов Урок"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsOwner | IsModer,)


class LessonListAPIView(generics.ListAPIView):
    """представление для просмотра объекта Урок"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsOwner | IsModer,)
    pagination_class = StudiesPagination


class LessonUpdateAPIView(generics.UpdateAPIView):
    """представление для редактирования объекта Урок"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsOwner | IsModer,)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """представление для удаления объекта Урок"""

    queryset = Lesson.objects.all()
    permission_classes = (IsOwner | ~IsModer,)


class SubscribeAPIView(APIView):
    """контроллер для управления подписками"""

    serializer_class = SubscribeSerializer
    queryset = Subscribe.objects.all()

    def post(self, request):
        user = request.user
        course_id = request.data.get('course')
        course = get_object_or_404(Course, id=course_id)
        subscribe = Subscribe.objects.filter(user=user, course=course).first()
        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subscribe:
            subscribe.delete()
            message = 'подписка удалена'
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscribe.objects.create(user=user, course=course)
            message = 'подписка добавлена'
        # Возвращаем ответ в API
        return Response({"message": message})
