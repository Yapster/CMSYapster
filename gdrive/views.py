from django.shortcuts import render
from oauth2client.django_orm import Storage
from gdrive.models import *
from gdrive.scripts import *

def home(request):
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    if storage:
        get_all_files(storage)