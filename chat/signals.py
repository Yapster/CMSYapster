from chat.models import *
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Message)
def new_message(sender, instance, created, **kwargs):
    if created:
        # Change Date last_created + notifications
        instance.conversation.date_last_message = datetime.now()
        instance.conversation.save()
        logger.warning()
    return