from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from admins.models import Profile, User, CmsUser, Announcement, GroupPermission
from admins.permissions import *
import logging

logger = logging.getLogger(__name__)


def login_user(request):
    """
    Display login page. Redirect to homepage if success

    TODO: Add yapster profile in session?
    """
    logout(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        current_user = authenticate(username=username, password=password)
        if current_user is not None:
            if current_user.is_active:
                login(request, current_user)
                #request.session['account'] = CmsUser.objects.get(user=current_user)
                return HttpResponseRedirect('/home/')
    return render(request, 'admins/login.html', {})

@login_required(login_url='/login/')
def cmsuser(request, username):
    """
    Display CMS user info + change permissions/name/username
    """
    cmsuser = CmsUser.objects.get(pk=request.user)
    own = cmsuser.username == username
    return render(request, 'admins/cmsuser.html', {"cmsuser": cmsuser, "own": own})


@login_required(login_url='/login/')
@user_passes_test(is_admin, login_url='/login/')
def users_manage(request):
    """
    List of users. Create and view users
    """
    users = CmsUser.objects.all()
    groups = GroupPermission.objects.all()
    if request.POST:
        logger.warning(request.POST)
        if request.POST['password'] == request.POST['password2']:
            username = request.POST['username']
            first = request.POST['firstname']
            last = request.POST['lastname']
            password = request.POST['password']
            email = request.POST['email']
            dep = request.POST['department']
            occ = request.POST['occupation']
            id_group = request.POST['group']
            group = GroupPermission.objects.get(pk=id_group)
            CmsUser.objects.get_or_create(username=username, firstname=first, lastname=last,
                                          email=email, password=password, department=dep, occupation=occ, group=group)
            return HttpResponseRedirect('/cmsusers/')
    return render(request, 'admins/users_manage.html',  {'users': users, 'groups':groups})


@login_required(login_url='/login/')
@user_passes_test(is_admin, login_url='/login/')
def annoucements_manage(request):
    announcements = Announcement.objects.all()
    if request.POST:
        title = request.POST['title']
        desc = request.POST['desc']
        Announcement.objects.get_or_create(user=request.user, title=title, description=desc)
        return HttpResponseRedirect('/announcements/')
    return render(request, 'admins/annoucements_manage.html', {"announcements": announcements})


@login_required(login_url='/login/')
def profile(request, username):
    """
    Display Yapster user profile. With info/stats
    """
    prof = Profile.objects.get(user__username=username)

    return render(request, 'admins/profile.html', {'profile': prof})


@login_required(login_url='/login/')
def edit_cmsuser(request, username):
    """
    Edit Cms User infos
    """

    cmsuser = CmsUser.objects.get(pk=request.user)
    firstname = lastname = email = password = ''
    if 'btn_newinfos' in request.POST:
        if request.POST['firstname']:
            cmsuser.firstname = request.POST['firstname']
        if request.POST['lastname']:
            cmsuser.lastname = request.POST['lastname']
        if request.POST['username']:
            cmsuser.username = request.POST['username']
        if request.POST['email'] and \
                request.POST['email2'] and \
                (request.POST['email'] == request.POST['email2']):
            cmsuser.email = request.POST['email']
        if request.POST['password'] and \
                request.POST['password2'] and \
                (request.POST['password'] == request.POST['password2']):
            cmsuser.password = request.POST['password']
        cmsuser.save()
    return render(request, 'admins/edit_cmsuser.html', {"cmsuser": cmsuser})