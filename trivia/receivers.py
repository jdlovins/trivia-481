from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Room


@receiver(pre_delete, sender=Room)
def pre_delete_room(sender, instance, **kwargs):
    for user in instance.users.all():
        user.delete()
