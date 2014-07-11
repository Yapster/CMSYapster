from tkinter.simpledialog import _QueryDialog
from django.shortcuts import render_to_response, render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from announcements.models import Announcement
from chat.models import Conversation, Message
from chat.signals import *
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@login_required(login_url='/login/')
@csrf_exempt
def homepage(request):
    """
    Display general stats
    """
    messages = []
    if 'chaters[]' in request.POST:
        # Get list of the users
        l_chaters = request.POST.getlist('chaters[]')
        if l_chaters == []:
            return False
        l_users = []
        for chater in l_chaters:
            l_users.append(User.objects.get(username=chater))
        l_users.append(request.user)
        # Get conversation with list of users
        query_conversation = Conversation.objects.annotate(count=Count('users')).filter(count=len(l_users))
        for user in l_users:
            query_conversation = query_conversation.filter(users__pk=user.pk)
        if not query_conversation:
            new_conversation = Conversation.objects.create()
            for user in l_users:
                new_conversation.users.add(user)
        else:
            current_conversation = query_conversation[0]
            current_conversation.date_last_message = datetime.now()
            current_conversation.save()
            messages = Message.objects.filter(conversation=current_conversation)
        conversations = Conversation.objects.filter(users=request.user).order_by('-date_last_message')

        return render(request, 'chat/messager.html', {"conversations": conversations,
                                                      "messages": messages})

    conversations = Conversation.objects.filter(users=request.user).order_by('-date_last_message')
    announcements = Announcement.objects.all()
    users = User.objects.exclude(username=request.user.username)
    current_conversation = None
    if 'conversation' in request.POST:
        # Get list of the users
        current_conversation = Conversation.objects.get(pk=request.POST['conversation'])
        if 'message' in request.POST:
            Message.objects.create(text=request.POST['message'], author=request.user, conversation=current_conversation)
        messages = Message.objects.filter(conversation=current_conversation)
        return render(request, 'chat/messager.html', {"messages": messages,
                                                      "conversations": conversations,
                                                      "current_conversation": current_conversation})
    if 'refresh' in request.POST:
        return render(request, 'chat/messager.html', {"messages": messages,
                                                      "conversations": conversations,
                                                      "current_conversation": current_conversation})

    return render(request, 'stats/home.html', {"announcements": announcements,
                                               "user": request.user,
                                               "chaters": users,
                                               "messages": messages,
                                               "conversations": conversations,
                                               "current_conversation": current_conversation})


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