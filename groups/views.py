from django.shortcuts import render
from django.http import HttpResponseRedirect
from groups.models import GroupPermission, Page
from admins.models import CmsUser
from admins.decorators import user_has_perm, active_and_login_required
from announcements.models import Announcement
from chat.models import Conversation, Message
from django.db.models import Count
from django.contrib.auth.models import User

@active_and_login_required
@user_has_perm
def group_manage(request):
    """
    Display permissions groups. Display members and pages for each
    """
    announcements = Announcement.objects.all()
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

    groups = GroupPermission.objects.filter(is_active=True)
    inactive_groups = GroupPermission.objects.filter(is_active=False)
    pages = Page.objects.all()
    if request.POST:
        if 'btn_deluser' in request.POST:
            cmsuser = CmsUser.objects.get(username=request.POST['user'])
            cmsuser.group = GroupPermission.objects.get(group_name="No Group")
            cmsuser.save()
        if 'btn_new' in request.POST:
            selected_pages = request.POST.getlist('page_selected')
            current_group = GroupPermission.objects.create(group_name=request.POST['groupname'])
            for id in selected_pages:
                page = Page.objects.get(pk=id)
                page.perms.add(current_group)
        if 'btn_delgroup' in request.POST:
            GroupPermission.objects.get(group_name=request.POST['group']).delete()
        if 'btn_active' in request.POST:
            # TODO: add Method in model : is_active + Signal Delete Group
            group_to_act = GroupPermission.objects.get(group_name=request.POST['group'])
            group_to_act.is_active = True
            group_to_act.save()
        return HttpResponseRedirect('')
    return render(request, 'admins/group_manage.html',
                  {"groups": groups, "inactive_groups": inactive_groups,
                   "pages": pages,
                   "announcements": announcements,
                   "user": request.user,
                   "chaters": users,
                   "messages": messages})

def group_details(request, group):
    announcements = Announcement.objects.all()
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


    g = GroupPermission.objects.get(group_name=group)

    return render(request, 'admins/group_details.html',
                  {"group": g,
                   "announcements": announcements,
                   "user": request.user,
                   "chaters": users,
                   "messages": messages})