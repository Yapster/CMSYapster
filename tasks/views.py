from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from admins.decorators import active_and_login_required
from tasks.models import *

@active_and_login_required
@csrf_exempt
def tasks(request):
    todo_tasks = Task.objects.filter(status='TO')
    inprogress_tasks = Task.objects.filter(status='IP')
    done_tasks = Task.objects.filter(status='DO')

    return render(request,
                  "tasks/home.html",
                  {"todo_tasks": todo_tasks,
                   "inprogress_tasks": inprogress_tasks,
                   "done_tasks": done_tasks
                  })

@csrf_exempt
@active_and_login_required
def update_task(request):
    t = Task.objects.get(pk=request.POST['taskId'])
    if request.POST['typeTask'] == 'inprogress':
        t.status = 'IP'
    elif request.POST['typeTask'] == 'todo':
        t.status = 'TO'
    else:
        t.status = 'DO'
    t.save()

    return render(request,
                  "tasks/task.html",
                  {"task": t})