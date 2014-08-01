from django.shortcuts import render
from django.http import HttpResponseRedirect
from announcements.models import Announcement
from django.db.models import Count
from django.contrib.auth.models import User
from chat.models import Conversation, Message
from admins.decorators import user_has_perm, active_and_login_required


@active_and_login_required
@user_has_perm
def annoucements_manage(request):
    announcements = Announcement.objects.order_by('-date_created')
    users = User.objects.exclude(username=request.user.username)
    conversations = Conversation.objects.filter(users=request.user).order_by('-date_last_message')

    if request.POST:
        title = request.POST['title']
        desc = request.POST['desc']
        Announcement.objects.get_or_create(user=request.user,
                                           title=title,
                                           description=desc)
        return HttpResponseRedirect('/announcements/')
    return render(request, 'admins/annoucements_manage.html',
                  {"announcements": announcements,
                   "user": request.user,
                   "conversations": conversations,
                   "chaters": users})


def announcements(request):
    announcements = Announcement.objects.all().order_by('-date_created')
    users = User.objects.exclude(username=request.user.username)
    conversations = Conversation.objects.filter(users=request.user).order_by('-date_last_message')

    return render(request,
                  'announcements/announcements.html',
                  {"announcements": announcements,
                   "conversations": conversations,
                   "chaters": users})