# app/management/commands/cleanup_sessions.py
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.sessions.models import SessionModel


class Command(BaseCommand):
    help = "Видаляє старі сесії разом з квитками"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_sessions = SessionModel.objects.filter(end_time__lt=now)
        count = expired_sessions.count()
        expired_sessions.delete()
        self.stdout.write(self.style.SUCCESS(f"Видалено {count} сесій"))
