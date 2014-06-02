from django.db import models

class GroupPermission(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=24, unique=True)
    is_active = models.BooleanField(default=True)

    def delete(self, using=None):
        self.is_active = False
        self.save()
        return


class Page(models.Model):
    page_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=24, unique=True)
    url = models.CharField(max_length=24, unique=True)
    description = models.CharField(max_length=24, blank=True)
    perms = models.ManyToManyField(to=GroupPermission, related_name='pages')
