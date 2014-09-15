from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from groups.models import GroupPermission, Page
from admins.models import CmsUser
from admins.decorators import user_has_perm, active_and_login_required
from announcements.models import Announcement
from chat.models import Conversation, Message
from django.db.models import Count
from django.contrib.auth.models import User, Group, Permission

@active_and_login_required
@permission_required('auth.group_management', login_url='/login/')
def group_manage(request):
    """
    Display permissions groups. Display members and pages for each
    """
    announcements = Announcement.objects.all()
    users = User.objects.all()
    groups = Group.objects.all()
    perms = Permission.objects.all()
    errors = []
    if request.POST:
        if 'btn_new' in request.POST:
            if request.POST['groupname'] == "":
                errors.append("Group Name empty")
            elif not request.POST.getlist('page_selected'):
                errors.append("No Pages selected")
            else:
                selected_pages = request.POST.getlist('page_selected')
                current_group = Group.objects.create(name=request.POST['groupname'])
                for id in selected_pages:
                    current_group.permissions.add(Permission.objects.get(pk=id))
        if 'btn_delgroup' in request.POST:
            Group.objects.get(pk=request.POST['group']).delete()
        if 'btn_active' in request.POST:
            # TODO: add Method in model : is_active + Signal Delete Group
            group_to_act = GroupPermission.objects.get(group_name=request.POST['group'])
            group_to_act.is_active = True
            group_to_act.save()
    return render(request, 'admins/group_manage.html',
                  {"announcements": announcements,
                   "user": request.user,
                   "errors" : errors,
                   "users": users,
                   "groups": groups,
                   "perms": perms})

def group_details(request, group):
    announcements = Announcement.objects.all()

    g = GroupPermission.objects.get(group_name=group)

    return render(request, 'admins/group_details.html',
                  {"group": g,
                   "announcements": announcements,
                   "user": request.user})