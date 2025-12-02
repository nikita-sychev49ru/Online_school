from celery import shared_task
from datetime import timedelta
from users.models import User
from django.utils import timezone


@shared_task
def last_login_check():
    """Проверяет, когда пользователь входил на сайт в последний раз.
    Тех, кто не входил давно блокирует."""
    users = User.objects.all()
    if users:
        for u in users:
            if u.last_login is None:
                if u.date_joined <= timezone.now() - timedelta(days=30):
                    u.is_active = False
                    u.save()
                    print(f"Пользователь {u.email} заблокирован")
            else:
                if u.last_login >= timezone.now() - timedelta(days=30):
                    u.is_active = False
                    u.save()
                    print(f"Пользователь {u.email} заблокирован")
