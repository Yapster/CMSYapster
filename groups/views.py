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
                   "user": request.user})

def group_details(request, group):
    announcements = Announcement.objects.all()

    g = GroupPermission.objects.get(group_name=group)

    return render(request, 'admins/group_details.html',
                  {"group": g,
                   "announcements": announcements,
                   "user": request.user})