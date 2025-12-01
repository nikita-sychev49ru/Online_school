from rest_framework import serializers

from studies.models import Course, Lesson, Subscribe
from studies.validators import VideoUrlValidator
from users.models import Payment


class LessonSerializer(serializers.ModelSerializer):
    """сериализатор для урока"""

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            VideoUrlValidator(field=['title', 'description', 'video_url']),
        ]


class CourseSerializer(serializers.ModelSerializer):
    """сериализатор для курса"""

    # получаем признак доступности курса для пользователя
    is_available = serializers.SerializerMethodField()

    def get_is_available(self, obj):
        request = self.context.get('request')
        return Payment.objects.filter(user=request.user, paid_course=obj).exists()

    # получаем признак подписки пользователя на курс
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        """Проверяем подписку текущего пользователя на курс"""
        request = self.context.get('request')
        return Subscribe.objects.filter(user=request.user, course=obj).exists()

    # получаем уроки, включенные в курс
    lessons = LessonSerializer(many=True, read_only=True)

    # получаем количество уроков в курсе
    lessons_count = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = '__all__'
        validators = [
            VideoUrlValidator(field=['title', 'description']),
        ]


class SubscribeSerializer(serializers.ModelSerializer):
    """сериализатор для подписки на курс"""

    class Meta:
        model = Subscribe
        fields = '__all__'
        read_only_fields = ('user', 'created_at')
