from email.quoprimime import _max_append
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=24)
    color = models.CharField(max_length=6)
    owner_category = models.ForeignKey(to=User, related_name='tasks_categories')
    is_public = models.BooleanField(default=False)



class TaskManager(models.Manager):
    def new_task(self, **kwargs):
        workers = []
        try:
            for w in kwargs.pop('workers'):
                workers.append(User.objects.get(pk=int(w)))
        except:
            pass
        new = self.create(**kwargs)
        for worker in workers:
            new.workers.add(worker)
        return new


class Task(models.Model):
    TODO = 'TO'
    IN_PROGRESS = 'IP'
    DONE = 'DO'
    STATUS_CHOICES = (
        (TODO, 'Todo'),
        (IN_PROGRESS, 'In Progress'),
        (DONE, 'Done'),
    )
    task_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=24)
    description = models.CharField(max_length=255, blank=True, null=True)
    workers = models.ManyToManyField(to=User, related_name='workers')
    category = models.ForeignKey(to=Category, related_name='category')
    deadline = models.DateTimeField(auto_now=True)
    priority = models.IntegerField(max_length=1, default=0)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=TODO)
    is_public = models.BooleanField(default=False)
    objects = TaskManager()



class TaskNote(models.Model):
    task_note_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(to=User, related_name='task_note_owner')
    task = models.ForeignKey(to=Task, related_name='task')
    text_note = models.CharField(max_length=255)
    date_last = models.DateTimeField(auto_now=True)