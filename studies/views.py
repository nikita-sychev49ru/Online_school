from rest_framework import viewsets, generics

from studies.models import Course, Lesson
from studies.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """вьюсет представлений для объектов модели Курс"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    """представление для создания объекта Урок"""
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """представление для просмотра списка объектов модели Урок"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonListAPIView(generics.ListAPIView):
    """представление для просмотра объекта Урок"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    """представление для редактирования объекта Урок"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    """представление для удаления объекта Урок"""
    queryset = Lesson.objects.all()