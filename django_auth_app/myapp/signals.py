from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserSettings

@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'settings'):
        UserSettings.objects.create(user=instance)
