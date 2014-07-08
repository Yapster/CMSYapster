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
    messages = []
    if 'chaters[]' in request.POST:
        # Get list of the users
        l_chaters = request.POST.getlist('chaters[]')
        l_users = []
        for chater in l_chaters:
            l_users.append(User.objects.get(username=chater))
        l_users.append(request.user)
        # Get conversation with list of users
        query_conversation = Conversation.objects.annotate(count=Count('users')).filter(count=len(l_users))
        for user in l_users:
            query_conversation = query_conversation.filter(users__pk=user.pk)
        if not query_conversation:
            current_conversation = Conversation.objects.create()
            for user in l_users:
                current_conversation.users.add(user)
        else:
            current_conversation = query_conversation[0]
            # If new message add
        if 'message' in request.POST:
            Message.objects.create(text=request.POST['message'], author=request.user, conversation=current_conversation)
        messages = Message.objects.filter(conversation=current_conversation)
        return render(request, 'chat/messages.html', {"messages": messages})
    if 'refresh' in request.POST:
        return render(request, 'chat/messages.html', {"messages": messages})
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
                   "chaters": users,
                   "messages": messages})
