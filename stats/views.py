from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from announcements.models import Announcement
from chat.models import Conversation, Message
from stats.models import Hashtag, Group
import socket
import logging

logger = logging.getLogger(__name__)

@login_required(login_url='/login/')
@csrf_exempt
def homepage(request):
    """
    Display general stats
    """
    announcements = Announcement.objects.all()
    users = User.objects.all()
    conversations = Conversation.objects.all()
    current_conversation = Conversation.objects.get(pk=1)
    messages = Message.objects.filter(conversation=current_conversation)
    if request.POST:
        logger.warning(request.POST)
        message = request.POST['message']
        Message.objects.create(text=message, author=request.user, conversation=current_conversation)
        response_dict = {}
        response_dict.update({'messages': messages})
        return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
    return render(request, 'stats/home.html', {"announcements": announcements,
                                               "user": request.user,
                                               "chaters": users,
                                               "conversations": conversations,
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