from django.shortcuts import render
from django.db.models import Count
from django.contrib.auth.models import User
from admins.decorators import active_and_login_required
from chat.models import Conversation, Message
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt


@active_and_login_required
@csrf_exempt
def chat(request):
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
                                                      "messages": messages,
                                                      "active": True})

    conversations = Conversation.objects.filter(users=request.user).order_by('-date_last_message')

    current_conversation = None
    if 'conversation' in request.POST:
        # Get list of the users
        current_conversation = Conversation.objects.get(pk=request.POST['conversation'])
        if 'message' in request.POST:
            Message.objects.create(text=request.POST['message'], author=request.user, conversation=current_conversation)
        messages = Message.objects.filter(conversation=current_conversation)
        return render(request, 'chat/messager.html', {"messages": messages,
                                                      "conversations": conversations,
                                                      "current_conversation": current_conversation,
                                                      "active": True})
    if 'refresh' in request.POST:
        return render(request, 'chat/messager.html', {"messages": messages,
                                                      "conversations": conversations,
                                                      "current_conversation": current_conversation,
                                                      "active": True})