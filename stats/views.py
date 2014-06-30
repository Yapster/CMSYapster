from django.shortcuts import render_to_response, render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from announcements.models import Announcement
from chat.models import Conversation, Message
from stats.models import Hashtag, Group
import logging

logger = logging.getLogger(__name__)

@login_required(login_url='/login/')
@csrf_exempt
def homepage(request):
    """
    Display general stats
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
    return render(request, 'stats/home.html', {"announcements": announcements,
                                               "user": request.user,
                                               "chaters": users,
                                               "messages": messages})


@login_required(login_url='/login/')
def stats(request):
    return render(request, 'stats/statistics.html', {})


@login_required(login_url='/login/')
def search(request):
    """
    Display research view
    """

    if request.POST:
        searchexp = request.POST['searchexp']
        postdate = request.POST['postdate']
        birthday = request.POST['birthday']
        numbers = request.POST['numbers']
        registerdate = request.POST['registerdate']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']


    return render(request, 'stats/index.html',{})


@login_required(login_url='/login/')
def hashtag(request, tag):
    """
    Display hashtag with count of people that used it and few yaps
    """
    current_tag = Hashtag.objects.get(name=tag)
    return render(request, 'stats/hashtag.html', {'tag': current_tag})


@login_required(login_url='/login/')
def group_page(request, group):
    """
    Display group page with count people in it and few yaps
    """
    current_group = Group.objects.get(pk=group)
    return render(request, 'stats/group.html', {'group': current_group})