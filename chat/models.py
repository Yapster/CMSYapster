from django.db import models
from users.models import User


class Conversation(models.Model):
    """
    Chat Room
    TODO Add who started the conv
    seed
    """
    conversation_id = models.AutoField(primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_message = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(to=User, related_name='users')
    is_active = models.BooleanField(default=True)

    def delete(self, using=None):
        self.is_active = False
        self.save()
        return

class Message(models.Model):
    """
    Message in a conversation
    """
    message_id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=128, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to=User, related_name="author")
    conversation = models.ForeignKey(to=Conversation, related_name="conversation")
    is_active = models.BooleanField(default=True)

    def delete(self, using=None):
        self.is_active = False
        self.save()
        return