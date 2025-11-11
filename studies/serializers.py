from rest_framework import serializers

from studies.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """сериалайзер для курса"""
    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    """сериалайзер для урока"""
    class Meta:
        model = Lesson
        fields = '__all__'