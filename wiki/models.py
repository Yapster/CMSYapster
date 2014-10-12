from annoying import models
from django.db import models
from django.contrib.auth.models import User

# class WikiPhoto(models.Model):
#     id = models.AutoField(primary_key=True)
from south.creator.freezer import model_dependencies


class WikiTag(models.Model):
    """
    Tag for the wiki pages
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)


class WikiCategory(models.Model):
    """
    Category for the wiki pages
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    linked_categories = models.ManyToManyField(to="WikiCategory", related_name="+")


class WikiPage(models.Model):
    """
    Wiki page. New one each modification
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    tags = models.ManyToManyField(WikiTag, related_name='pages')
    categories = models.ManyToManyField(WikiCategory, related_name='pages')
    is_current = models.BooleanField(default=True)
    father = models.ForeignKey(to='WikiPage',null=True, blank=True, related_name='sons')
    children = models.ManyToManyField(to='WikiPage', null=True, blank=True, related_name='+')
    favorites_users = models.ManyToManyField(User, related_name='favorites')
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # Override save to create a new page
    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     return


class WikiFolder(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, related_name='favorites_folders')
    articles = models.ManyToManyField(WikiPage, related_name='folders')


class WikiSection(models.Model):
    """
    Section if a wiki page. New section each modification
    """
    id = models.AutoField(primary_key=True)
    page = models.ForeignKey(WikiPage, related_name='sections')
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=1024)
    writer = models.ForeignKey(User, related_name='sections')
    order = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    is_current = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
    # Override save to create new section
    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     return