import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.db.models import URLField

from studies.models import Course, Lesson


class User(AbstractUser):
    username = models.CharField(max_length=50, blank=True, null=True, unique=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, verbose_name="Телефон", blank=True, null=True)
    city = models.CharField(max_length=50, verbose_name="Город", blank=True, null=True)
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
        ordering = [
            "email",
        ]


class Payment(models.Model):
    """модель платежа за курсы или уроки"""

    CASH = "наличные"
    TRANSFER = "перевод на счет"
    STRIPE = "Stripe онлайн-оплата"

    METHOD_CHOICES = [(CASH, "наличные"), (TRANSFER, "перевод на счет"), (STRIPE, "Stripe онлайн-оплата")]

    PENDING = "Ожидает оплаты"
    PAID = "Оплачено"
    FAILED = "Ошибка оплаты"
    REFUNDED = "Возвращено"

    STATUS_CHOICES = [
        (PENDING, "Ожидает оплаты"),
        (PAID, "Оплачено"),
        (FAILED, "Ошибка оплаты"),
        (REFUNDED, "Возвращено"),
    ]

    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, verbose_name='публичный ID')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='payments', blank=True, null=True, verbose_name='пользователь'
    )
    payment_date = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='дата создания платежа')
    paid_date = models.DateTimeField(blank=True, null=True, verbose_name='дата оплаты')
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='payments',
        blank=True,
        null=True,
        verbose_name='оплаченный курс',
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='payments',
        blank=True,
        null=True,
        verbose_name='оплаченный урок',
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, blank=True, verbose_name='сумма оплаты'
    )
    payment_method = models.CharField(
        max_length=20, choices=METHOD_CHOICES, default=STRIPE, verbose_name='способ оплаты'
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=PENDING, verbose_name='статус платежа')
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID сессии Stripe')
    link = URLField(max_length=400, blank=True, null=True, verbose_name='ссылка на оплату')

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        indexes = [
            models.Index(fields=['public_id']),
        ]
        ordering = [
            '-payment_date',
        ]
        db_table = 'payments'

    def __str__(self):
        if self.paid_course:
            return f'Платеж от {self.user} за обучающий материал {self.paid_course} на сумму {self.amount} руб.'
        return f'Платеж от {self.user} за обучающий материал {self.paid_lesson} на сумму {self.amount} руб.'
