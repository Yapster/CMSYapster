from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpRequest, HttpResponseRedirect
from functools import wraps
from admins.models import CmsUser


def permission(permission_tester, login_url="/login/"):
    @wraps(permission_tester)
    def view_decorator(view_function):
        @wraps(view_decorator)
        def decorated_view(request, *args, **kwargs):
            if permission_tester(request, *args, **kwargs):
                view_result = view_function(request, *args, **kwargs)
            else:
                view_result = HttpResponseRedirect(login_url)
            return view_result
        return decorated_view
    return view_decorator

@permission
def user_has_perm(request, username=None):
    """
    Check if user has perm via group permission
    """
    if username == request.user.username:
        return True
    path = request.path
    cmsuser = CmsUser.objects.get(pk=request.user)
    if cmsuser.group.group_name == "Admin":
        return True
    perms = cmsuser.group.pages.all()
    for page in perms:
        if page.url == path:
            return True
    return False

active_required = user_passes_test(lambda u: u.is_active,
                                   login_url='/login/')


def active_and_login_required(view_func):
    decorated_view_func = login_required(active_required(view_func), login_url='/login/')
    return decorated_view_func