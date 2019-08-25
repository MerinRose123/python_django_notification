from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Like


@receiver(post_save, sender=User)
def announce_new_user(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "gossip", {"type": "user.gossip",
                       "event": "New User",
                       "username": instance.username})


@receiver(post_delete, sender=User)
def post_delete_handler(sender, instance, **kwargs):
    """
    Called when row is deleted.
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "gossip", {"type": "user.gossip",
                   "event": "Delete User",
                   "username": instance.username})


'''
@receiver(post_save, sender=Like)
def announce_like(sender, instance,created, **kwargs):
    if created:
        channel_layer=get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "liked", {"type": "user.like",
                      "event": "like",
                      "username": "instance.username"
                      }
        )
'''