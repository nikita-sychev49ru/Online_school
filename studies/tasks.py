from celery import shared_task


@shared_task
def send_course_update_email(course_id):
    """отправка письма об обновлении курса для подписчика"""
    from django.core.mail import send_mail
    from studies.models import Subscribe
    from config import settings

    subs = Subscribe.objects.filter(course_id=course_id).select_related('user', 'course')
    if subs.exists():
        course_title = subs[0].course.title
        recipient_list = [sub.user.email for sub in subs if sub.user.email]

        send_mail(
            subject="Обновления курса",
            message=f"Появились обновления в рамках курса {course_title}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=False,
        )
