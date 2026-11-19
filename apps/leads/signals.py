from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Lead
from .notifications import notify_managers_about_lead


@receiver(post_save, sender=Lead, dispatch_uid="leads.notify_managers_about_new_lead")
def notify_managers_about_new_lead(sender, instance, created, **kwargs):
    if created:
        notify_managers_about_lead(instance)
