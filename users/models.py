from django.contrib.auth.models import AbstractUser
from django.db import models

from studies.models import Course, Lesson


class User(AbstractUser):
    username = models.CharField(max_length=50, blank=True, null=True, unique=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=15, verbose_name="Телефон", blank=True, null=True
    )
    city = models.CharField(
        max_length=50, verbose_name="Город", blank=True, null=True
    )
    avatar = models.ImageField(
        upload_to="images/",
        default="images/placeholder.png",
        verbose_name="Аватар",
        blank=True,
        null=True,
    )


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        ordering = ["email",]


class Payment(models.Model):
    """модель платежа за курсы или уроки"""
    CASH = "наличные"
    TRANSFER = "перевод на счет"

    METHOD_CHOICES = [
        (CASH, "наличные"),
        (TRANSFER, "перевод на счет"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', blank=True, null=True, verbose_name='пользователь')
    payment_date = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='дата оплаты')
    paid_course = models.ManyToManyField(Course, related_name='payments', blank=True, verbose_name='оплаченный курс')
    paid_lesson = models.ManyToManyField(Lesson, related_name='payments', blank=True, verbose_name='оплаченный урок')
    amount = models.FloatField(blank=True, null=True, verbose_name='сумма оплаты')
    payment_method = models.CharField(max_length=15, choices=METHOD_CHOICES, default=CASH, verbose_name='способ оплаты',)


    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        ordering = ['user', 'payment_date',]
        db_table = 'payments'



    def __str__(self):
        if self.paid_course:
            return f'Оплата от {self.user} за курс {self.paid_course}. Сумма - {self.amount} (получено {self.payment_date})'
        return f'Оплата от {self.user} за курс {self.paid_lesson}. Сумма - {self.amount} (получено {self.payment_date})'