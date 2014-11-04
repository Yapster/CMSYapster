from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from admins.decorators import active_and_login_required
from tasks.models import *
from django.db.models import Q

@active_and_login_required
@csrf_exempt
def tasks(request):
    todo_tasks = Task.objects.filter(Q(is_public=True)|Q(workers=request.user), status='TO')
    inprogress_tasks = Task.objects.filter(Q(is_public=True)|Q(workers=request.user), status='IP')
    done_tasks = Task.objects.filter(Q(is_public=True)|Q(workers=request.user), status='DO')
    users = User.objects.all()
    categories = Category.objects.all()

    return render(request,
                  "tasks/home.html",
                  {"todo_tasks": todo_tasks,
                   "inprogress_tasks": inprogress_tasks,
                   "done_tasks": done_tasks,
                   "user": request.user,
                   "users": users,
                   "categories": categories})

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

@csrf_exempt
def new_note(request):
    note = None
    if request.POST:
        kwargs = {
            'owner': request.user,
            'task': Task.objects.get(pk=request.POST['taskId']),
            'text_note': request.POST['note_text']
        }
        note = TaskNote.objects.create(**kwargs)
    return render(request,
                  "tasks/new_note.html",
                  {"note":note,
                   "user": request.user})

@csrf_exempt
def save_members(request):
    t = Task.objects.get(pk=request.POST['taskId'])
    l = request.POST.getlist('members[]')
    if l:
        for u in t.workers.all():
            t.workers.remove(u)
        for m in l:
            t.workers.add(m)
    return render(request,
                  "tasks/new_note.html",{})