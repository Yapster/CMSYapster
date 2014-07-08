import boto
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.conf import settings
from admins.models import CmsUser, Profile
from chat.models import Conversation
import logging

logger = logging.getLogger(__name__)


class File(models.Model):
    """
    Abstract Class for File
    """

    file_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    path = models.CharField(max_length=128, unique=True)

    def delete(self, using=None):
        self.is_active = False
        self.save()

    class Meta:
        abstract = True


class ProfilePicture(File):
    """
    Profile Pictures for a user
    """

    user_id = models.ForeignKey(to=User)
    is_current = models.BooleanField(default=False)

class ConversationPicture(File):
    """
    File shared within a conversation
    """

    conversation_id = models.ForeignKey(Conversation)


class FileManager(models.Model):
    """
    File Management. Up/Download
    """

    #TODO: Optimized
    @staticmethod
    def store(path_bucket, content, filename, file_type=None, user=None):
        """
        Store the file into S3. Return Something if success/ False if not
        """
        c = boto.connect_s3()
        b = c.get_bucket(settings.BUCKET_NAME)
        if b:
            k = b.get_key(path_bucket)
            if not k:
                k = b.new_key(path_bucket)
                k.set_contents_from_string(content)
                if  file_type == "profile":
                    try:
                        old_pix = ProfilePicture.objects.get(is_current=True)
                        old_pix.is_current = False
                        old_pix.save()
                    except:
                        pass
                    ProfilePicture.objects.create(name=filename, path=path_bucket, user_id=user, is_current=True)
        return

    @staticmethod
    def get_profile_picture(user):
        """
        Get a file from S3
        """
        c = boto.connect_s3()
        b = c.get_bucket(settings.BUCKET_NAME)
        if b:
            p = ProfilePicture.objects.get(is_current=True, user_id=user)
            s3_file_path = b.get_key(p.path)
            return s3_file_path.generate_url(expires_in=600)
        return ""


    @staticmethod
    def get_all_profile_pictures(pictures):
        """
        Get all profile pictures from a user
        """
        c = boto.connect_s3()
        b = c.get_bucket(settings.BUCKET_NAME)
        if b:
            urls = []
            for picture in pictures:
                s3_file_path = b.get_key(picture.path)
                urls.append(s3_file_path.generate_url(expires_in=600))
            return urls
        return []


class FileForm(forms.Form):
    name = models.CharField(max_length=64)
    file = models.FileField()