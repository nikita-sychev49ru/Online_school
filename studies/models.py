from tkinter.constants import CASCADE

from django.db import models

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

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'
        ordering = ['title',]
        db_table = 'courses'


    def __str__(self):
        return self.title


class Lesson(models.Model):
    """модель урока из обучающего курса"""
    title = models.CharField(max_length=150, verbose_name='название урока')
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='порядковый номер'
    )
    description = models.TextField(blank=True, null=True, verbose_name='описание урока')
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

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        ordering = ['course', 'order',]
        db_table = 'lessons'


    def __str__(self):
        return f'{self.title} (курс: {self.course})'