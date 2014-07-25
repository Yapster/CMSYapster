from django.shortcuts import render
from contacts.models import Note, List, Contact
from admins.models import CmsUser
from django.db.models import Count
from django.contrib.auth.models import User
from announcements.models import Announcement
from chat.models import Conversation, Message
from files_manager.models import FileManager
from cms_location.models import *

def contacts_lists(request):
    lists = List.objects.filter(is_active=True)
    inactive_lists = List.objects.filter(is_active=False)
    inactive_contacts = Contact.objects.filter(is_active=False)
    if 'btn_delgroup' in request.POST:
        l = List.objects.get(name=request.POST['list'])
        l.delete()
    if 'btn_active' in request.POST:
        l = List.objects.get(name=request.POST['list'])
    countries = CmsCountry.objects.all()
    cities = CmsCity.objects.all()
    zip_codes = CmsUSZIPCode.objects.all()
    states = CmsUSState.objects.all()
    return render(request,
                  'contacts/lists.html',
                  {'lists': lists,
                   'inactive_lists': inactive_lists,
                   'inactive_contacts': inactive_contacts,
                   "user": request.user,
                   "countries": countries,
                   "cities": cities,
                   "zip_codes": zip_codes,
                   "states": states})


def contacts_lists_details(request, list):
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

    l = List.objects.get(pk=list)
    return render(request, 'contacts/list_details.html', {'list': l,
                                                          "announcements": announcements,
                                                          "user": request.user,
                                                          "chaters": users,
                                                          "messages": messages})


def contacts_details(request, list, contact):
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

    c = Contact.objects.get(pk=contact)
    if 'btn_newnote' in request.POST:
        Note.objects.create(description=request.POST['newnote'],
                            author=request.user,
                            contact=c)
    url_profile_picture = FileManager.get_profile_picture(request.user)
    return render(request, 'contacts/contact_details.html', {'contact': c,
                                                             "announcements": announcements,
                                                             "user": request.user,
                                                             "chaters": users,
                                                             "messages": messages,
                                                             "url_profile_picture": url_profile_picture})