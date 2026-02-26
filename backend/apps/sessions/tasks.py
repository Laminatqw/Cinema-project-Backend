from django.utils import timezone

from celery import shared_task

from .models import SessionModel


@shared_task
def update_sessions_status():
    """Міняємо статус сесій на completed, якщо вони вже закінчились."""
    now = timezone.now()
    sessions = SessionModel.objects.filter(end_time__lt=now, is_active=True)
    count = sessions.update(status="completed")
    return f"Updated {count} sessions"


@shared_task
def clean_old_sessions():
    """Видаляємо сесії старші 30 днів разом із квитками."""
    now = timezone.now()
    old_sessions = SessionModel.objects.filter(end_time__lt=now - timezone.timedelta(days=30))
    count = old_sessions.count()
    old_sessions.delete()
    return f"Deleted {count} old sessions"
