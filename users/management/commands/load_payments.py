import os
import random
from datetime import datetime, timedelta

from django.core.management import BaseCommand, call_command

from studies.models import Course, Lesson
from users.models import User, Payment


class Command(BaseCommand):
    help = "заполняет БД объектами модели платеж, создает по 3 объекта с рандомными данными за один запуск"

    def handle(self, *args, **options):
        count = 3

        courses = Course.objects.all()
        lessons = Lesson.objects.all()
        users = User.objects.all()

        payment_methods = [Payment.CASH, Payment.TRANSFER]
        created_count = 0

        for i in range(count):
            try:
                # случайный пользователь
                user = random.choice(users)
                # случайная дата (последние 30 дней)
                payment_date = datetime.now() - timedelta(days=random.randint(0, 30))
                # случайный метод оплаты
                payment_method = random.choice(payment_methods)
                # создаем объект модели платеж
                payment = Payment.objects.create(
                    user=user,
                    amount = 0.00,
                    payment_date=payment_date,
                    payment_method=payment_method
                )

                # добавляем случайный курс или урок
                has_course_or_lesson = False
                amount = 0.00

                if courses and random.choice([True, False]):
                    paid_course = random.choice(courses)
                    payment.paid_course = Course.objects.get(pk=paid_course.pk)
                    amount = paid_course.price
                    Course.objects.filter(pk=paid_course.pk).update(is_available=True)
                    has_course_or_lesson = True

                if lessons.exists() and random.choice([True, False]):
                    paid_lesson = random.choice(lessons)
                    payment.paid_lesson = Lesson.objects.get(pk=paid_lesson.pk)
                    amount = paid_lesson.price
                    Lesson.objects.filter(pk=paid_lesson.pk).update(is_available=True)
                    has_course_or_lesson = True

                if has_course_or_lesson:
                    payment.amount = amount
                    payment.save()
                    created_count += 1

                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Создан платеж #{created_count}: {user.username} - {payment.amount} руб.'
                        )
                    )

                else:
                    payment.delete()

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Ошибка при создании платежа: {e}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Успешно создано {created_count} платежей из {count} запланированных'
            )
        )