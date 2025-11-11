from rest_framework import serializers

from studies.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """сериализатор для урока"""
    class Meta:
        model = Lesson
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    """сериализатор для курса"""
    # получаем уроки, включенные в курс
    lessons = LessonSerializer(many=True)

    # получаем количество уроков в курсе
    lessons_count = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ['title', 'preview', 'description', 'lessons_count', 'lessons']