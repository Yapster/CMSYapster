from django.contrib.comments.views.comments import post_comment
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from admins.models import CmsUser
from admins.decorators import user_has_perm, active_and_login_required
from admins.signals import *
from django.db.models import Count
from django.contrib.auth.models import User
from chat.models import Conversation, Message
from files_manager.models import FileManager, FileForm, ProfilePicture
from users.models import *
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
        current_cms_user = CmsUser.objects.get(pk=current_user)
        if current_cms_user is not None:
            if current_cms_user.is_active:
                login(request, current_user)
                response = HttpResponseRedirect('/home/')
                #request.session['account'] = CmsUser.objects.get(user=current_user)
                return response
    return render(request, 'admins/login.html', {})


@active_and_login_required
@user_has_perm
def users_manage(request):
    """
    List of users. Create and view users
    """

    users_managed = CmsUser.objects.filter(is_active=True)
    inactive_users = CmsUser.objects.filter(is_active=False)
    groups = GroupPermission.objects.all()

    if 'btn_delete' in request.POST:
        username = request.POST['username']
        user = CmsUser.objects.get(username=username)
        user.is_active = False
        user.save()
        return HttpResponseRedirect('/cmsusers/')

    if 'btn_active' in request.POST:
        username = request.POST['username']
        user = CmsUser.objects.get(username=username)
        user.is_active = True
        user.save()
        return HttpResponseRedirect('/cmsusers/')

    if 'btn_new' in request.POST:
        if request.POST['password'] == request.POST['password2'] \
                and request.POST['email'] == request.POST['email2']:
            username = request.POST['username']
            first = request.POST['firstname']
            last = request.POST['lastname']
            password = request.POST['password']
            email = request.POST['email']
            dep = request.POST['department']
            occ = request.POST['occupation']
            id_group = request.POST['group']
            group = GroupPermission.objects.get(pk=id_group)
            CmsUser.new_user(username=username, first_name=first, last_name=last,
                             email=email, password=password, department=dep,
                             occupation=occ, group=group)
            return HttpResponseRedirect('/cmsusers/')
    return render(request, 'admins/users_manage.html',
                  {'users': users_managed,
                   'inactive_users': inactive_users,
                   'groups':groups,
                   "user": request.user})

@active_and_login_required
@user_has_perm
def cmsuser(request, username):
    """
    Display CMS user info + change permissions/name/username
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
    cmsuser = CmsUser.objects.get(username=username)
    own = cmsuser.username == username
    return render(request, 'admins/cmsuser.html',
                  {"cmsuser": cmsuser, "own": own,
                   "announcements": announcements,
                   "user": request.user,
                   "chaters": users,
                   "messages": messages})


@active_and_login_required
@user_has_perm
def edit_cmsuser(request, username):
    """
    Edit Cms User infos
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

    cmsuser = CmsUser.objects.get(username=username)
    d_args = {}
    if 'btn_newinfos' in request.POST:
        if request.POST['firstname']:
            d_args['first_name'] = request.POST['firstname']
        if request.POST['lastname']:
            d_args['last_name'] = request.POST['lastname']
        if request.POST['username']:
            d_args['username'] = request.POST['username']
        if request.POST['email'] and \
                request.POST['email2'] and \
                (request.POST['email'] == request.POST['email2']):
            d_args['email'] = request.POST['email']
        if request.POST['password'] and \
                request.POST['password2'] and \
                (request.POST['password'] == request.POST['password2']):
            d_args['password'] = request.POST['password']
        cmsuser.update(**d_args)
        return HttpResponseRedirect('')
    return render(request, 'admins/edit_cmsuser.html', {"cmsuser": cmsuser,
                                                        "announcements": announcements,
                                                        "user": request.user,
                                                        "chaters": users,
                                                        "messages": messages})


@active_and_login_required
def profile(request, username):
    """
    Display Yapster user profile. With info/stats
    """
    error = []
    cmsuser = CmsUser.objects.get(user__username=username)
    if 'username' in request.POST:
        try:
            u = User.objects.using('yte_1_db').get(username=request.POST['username'])
            cmsuser.yapster_user_id = u.id
            cmsuser.save()
        except:
            error.append("User not found")

    current_url = FileManager.get_profile_picture(request.user)
    profile = None
    userinfo = None
    yapster_account = None
    if cmsuser.yapster_user_id:
        profile = Profile.objects.get(user=cmsuser.yapster_user_id)
        userinfo = UserInfo.objects.get(user_id=cmsuser.yapster_user_id)
        yapster_account = User.objects.using('yte_1_db').get(pk=cmsuser.yapster_user_id)

    return render(request, 'admins/profile.html', {'cmsuser': cmsuser,
                                                   "profile": profile,
                                                   "userinfo": userinfo,
                                                   'url': current_url,
                                                   'yapster_account': yapster_account,
                                                   'error': error})

@active_and_login_required
@user_has_perm
@csrf_exempt
def edit_profile_pic(request, username):

    # Choose existing photo
    if 'new_photo' in request.POST:
        ex_pix = ProfilePicture.objects.get(is_current=True, user_id=request.user)
        ex_pix.is_current = False
        ex_pix.save()
        new_pix = ProfilePicture.objects.get(pk=request.POST['new_photo'])
        new_pix.is_current = True
        new_pix.save()

    # Add photo to Amazon
    if 'button_new_pic' in request.POST:
        # Pix getting upload
        # TODO: Check if valid image
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['new_pic']
            path_bucket = "yapstercmsusers/uid/" + str(CmsUser.objects.get(username=username).user_id) + "/profile_pictures/" + file.name
            FileManager.store(path_bucket, file.read(), file.name, "profile", request.user)

    # Get all pictures from user
    pictures = ProfilePicture.objects.filter(user_id=request.user)
    urls = FileManager.get_all_profile_pictures(pictures)
    current_url = FileManager.get_profile_picture(request.user)
    return render(request,
                  'admins/edit_profile_pic.html',
                  {"urls": urls.items(),
                   "current_url": current_url,
                   "pictures": pictures,
                   "user": request.user})