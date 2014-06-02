from django.shortcuts import render
from django.http import HttpResponseRedirect
from announcements.models import Announcement
from admins.decorators import user_has_perm, active_and_login_required


@active_and_login_required
@user_has_perm
def annoucements_manage(request):
    announcements = Announcement.objects.order_by('-date_created')
    if request.POST:
        title = request.POST['title']
        desc = request.POST['desc']
        Announcement.objects.get_or_create(user=request.user,
                                           title=title,
                                           description=desc)
        return HttpResponseRedirect('/announcements/')
    return render(request, 'admins/annoucements_manage.html',
                  {"announcements": announcements})
