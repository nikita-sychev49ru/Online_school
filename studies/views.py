from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from studies.models import Course, Lesson
from studies.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """вьюсет представлений для объектов модели Курс"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~IsModer,)
        elif self.action == 'destroy':
            self.permission_classes = (IsOwner,)
        elif self.action in ['retrieve', 'update']:
            self.permission_classes = (IsModer|IsOwner,)
        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    """представление для создания объекта Урок"""
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated & ~IsModer,)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """представление для просмотра списка объектов модели Урок"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsOwner|IsModer,)


class LessonListAPIView(generics.ListAPIView):
    """представление для просмотра объекта Урок"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsOwner|IsModer,)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """представление для редактирования объекта Урок"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsOwner|IsModer,)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """представление для удаления объекта Урок"""
    queryset = Lesson.objects.all()
    permission_classes = (IsOwner & ~IsModer,)