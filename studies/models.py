from django.db import models
from django.db.models import CASCADE

from config.settings import AUTH_USER_MODEL


class Course(models.Model):
    """модель обучающего курса"""

    title = models.CharField(max_length=150, verbose_name='название курса')
    preview = models.ImageField(
        upload_to='images/',
        default='images/placeholder.png',
        verbose_name='превью курса',
        blank=True,
        null=True,
    )
    description = models.TextField(blank=True, null=True, verbose_name='описание курса')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=999.99, verbose_name='стоимость курса')
    is_available = models.BooleanField(default=False, verbose_name='доступность')
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE, blank=True, null=True, verbose_name='владелец курса')

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'
        ordering = [
            'title',
        ]
        db_table = 'courses'

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """модель урока из обучающего курса"""

    title = models.CharField(max_length=150, verbose_name='название урока')
    order = models.PositiveIntegerField(default=0, verbose_name='порядковый номер')
    description = models.TextField(blank=True, null=True, verbose_name='описание урока')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=99.99, verbose_name='стоимость урока')

    preview = models.ImageField(
        upload_to='images/',
        default='images/placeholder.png',
        verbose_name='превью урока',
        blank=True,
        null=True,
    )
    video_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='ссылка на видео',
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='курс',
    )
    is_available = models.BooleanField(default=False, verbose_name='доступность')
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE, blank=True, null=True, verbose_name='владелец урока')

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        ordering = [
            'course',
            'order',
        ]
        db_table = 'lessons'

    def __str__(self):
        return f'{self.title} (курс: {self.course})'


class Subscribe(models.Model):
    """модель подписки на обучающий курс"""

    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=CASCADE, related_name='subscriptions', blank=True, verbose_name='пользователь'
    )
    course = models.ForeignKey(
        Course, on_delete=CASCADE, related_name='subscriptions', blank=True, verbose_name='курс'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        ordering = ['-created_at']
        db_table = 'subscribes'
        unique_together = [['user', 'course']]

    def __str__(self):
        return f'Подписка пользователя {self.user} на курс {self.course}'
