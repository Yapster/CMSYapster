from django.shortcuts import render_to_response, render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from announcements.models import Announcement
from chat.models import Conversation, Message
import logging

logger = logging.getLogger(__name__)

@login_required(login_url='/login/')
@csrf_exempt
def homepage(request):
    """
    Display general stats
    """
    conversations = Conversation.objects.filter(users=request.user).order_by('-date_last_message')
    announcements = Announcement.objects.all()
    users = User.objects.exclude(username=request.user.username)
    messages = []
    if 'conversation' in request.POST:
        # Get list of the users
        current_conversation = Conversation.objects.get(pk=request.POST['conversation'])
        if 'message' in request.POST:
            Message.objects.create(text=request.POST['message'], author=request.user, conversation=current_conversation)
        messages = Message.objects.filter(conversation=current_conversation)
        return render(request, 'chat/messages.html', {"messages": messages})
    if 'refresh' in request.POST:
        return render(request, 'chat/messages.html', {"messages": messages})
    return render(request, 'stats/home.html', {"announcements": announcements,
                                               "user": request.user,
                                               "chaters": users,
                                               "messages": messages,
                                               "conversations": conversations})


@login_required(login_url='/login/')
def stats(request):
    conversations = Conversation.objects.filter(users=request.user).order_by('-date_last_message')
    announcements = Announcement.objects.all()
    users = User.objects.exclude(username=request.user.username)
    messages = []
    if 'conversation' in request.POST:
        # Get list of the users
        current_conversation = Conversation.objects.get(pk=request.POST['conversation'])
        if 'message' in request.POST:
            Message.objects.create(text=request.POST['message'], author=request.user, conversation=current_conversation)
        messages = Message.objects.filter(conversation=current_conversation)
        return render(request, 'chat/messages.html', {"messages": messages})
    if 'refresh' in request.POST:
        return render(request, 'chat/messages.html', {"messages": messages})
    return render(request, 'stats/statistics.html', {"announcements": announcements,
                                                     "user": request.user,
                                                     "chaters": users,
                                                     "messages": messages,
                                                     "conversations": conversations})


@login_required(login_url='/login/')
def search(request):
    """
    Display research view
    """
    if 'search_button' in request.POST:
        searchexp = request.POST['searchexp']
        postdate = request.POST['postdate']
        birthday = request.POST['birthday']
        numbers = request.POST['numbers']
        registerdate = request.POST['registerdate']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']

    conversations = Conversation.objects.filter(users=request.user).order_by('-date_last_message')
    announcements = Announcement.objects.all()
    users = User.objects.exclude(username=request.user.username)
    messages = []
    if 'conversation' in request.POST:
        # Get list of the users
        current_conversation = Conversation.objects.get(pk=request.POST['conversation'])
        if 'message' in request.POST:
            Message.objects.create(text=request.POST['message'], author=request.user, conversation=current_conversation)
        messages = Message.objects.filter(conversation=current_conversation)
        return render(request, 'chat/messages.html', {"messages": messages})
    if 'refresh' in request.POST:
        return render(request, 'chat/messages.html', {"messages": messages})
    return render(request, 'stats/index.html',{"announcements": announcements,
                                               "user": request.user,
                                               "chaters": users,
                                               "messages": messages,
                                               "conversations": conversations})


    # @login_required(login_url='/login/')
    # def hashtag(request, tag):
    #     """
    #     Display hashtag with count of people that used it and few yaps
    #     """
    #
    #     current_tag = Hashtag.objects.get(name=tag)
    #     return render(request, 'stats/hashtag.html', {'tag': current_tag})
    #
    #
    # @login_required(login_url='/login/')
    # def group_page(request, group):
    #     """
    #     Display group page with count people in it and few yaps
    #     """
    #     current_group = Group.objects.get(pk=group)
    #     return render(request, 'stats/group.html', {'group': current_group})