from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from admins.models import Profile, User


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
                #request.session['profile'] = Profile.objects.get(user=current_user)
                return HttpResponseRedirect('/home/')
    return render_to_response('admins/login.html',
        {},
                            context_instance=RequestContext(request))


def cmsuser(request, username):
    """
    Display CMS user info + change permissions/name/username
    """
    return render_to_response('admins/cmsuser.html',
        {},
                              content_type=RequestContext(request))


def users_manage(request):
    """
    List of users. Create and view users
    """
    if 'btn_newuser' in request.POST:
        if request.POST['password'] == request.POST['repassword']:
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            User.objects._create_user(username, email, password, is_staff=False, is_superuser=False)
    return render_to_response('admins/users_manage.html',
        {},
                              content_type=RequestContext(request))


def annoucements_manage(request):
    return render_to_response('admins/annoucements_manage.html',
        {},
                              content_type=RequestContext(request))

def profile(request, username):
    """
    Display Yapster user profile. With info/stats
    """
    return render_to_response('admins/profile.html',
        {},
                              content_type=RequestContext(request))