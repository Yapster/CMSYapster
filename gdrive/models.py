from django.db import models
from django.contrib.auth.models import User
from oauth2client.django_orm import FlowField, CredentialsField

class FlowModel(models.Model):
    flow_id = models.ForeignKey(User, primary_key=True)
    flow = FlowField()

class CredentialsModel(models.Model):
    credentials_id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()