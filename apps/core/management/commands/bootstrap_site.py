import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.core.models import SiteSettings


class Command(BaseCommand):
    help = (
        "Idempotent first-run setup: creates the site settings row and, if "
        "DJANGO_SUPERUSER_USERNAME / DJANGO_SUPERUSER_PASSWORD are set, the admin user. "
        "Needed because Render's free plan has no shell."
    )

    def handle(self, *args, **options):
        SiteSettings.load()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        if not (username and password):
            self.stdout.write("Superuser variables are not set, skipping admin creation.")
            return

        User = get_user_model()
        if User.objects.filter(username=username).exists():
            self.stdout.write(f"Admin '{username}' already exists.")
            return
        User.objects.create_superuser(
            username=username,
            email=os.environ.get("DJANGO_SUPERUSER_EMAIL", ""),
            password=password,
        )
        self.stdout.write(self.style.SUCCESS(f"Admin '{username}' created."))
