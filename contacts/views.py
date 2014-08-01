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
    errors = []
    announcements = Announcement.objects.all()
    users = User.objects.exclude(username=request.user.username)
    conversations = Conversation.objects.filter(users=request.user).order_by('-date_last_message')
    lists = List.objects.filter(is_active=True)
    inactive_lists = List.objects.filter(is_active=False)
    inactive_contacts = Contact.objects.filter(is_active=False)

    countries = CmsCountry.objects.all()
    cities = CmsCity.objects.all()
    zip_codes = CmsUSZIPCode.objects.all()
    states = CmsUSState.objects.all()

    if 'btn_delgroup' in request.POST:
        l = List.objects.get(name=request.POST['list'])
        l.delete()
    if 'btn_active' in request.POST:
        List.objects.get(name=request.POST['list']).activate()
    if 'btn_active_contact' in request.POST:
        Contact.objects.get(pk=request.POST['inactive_contact']).activate()
    if 'btn_new_contact' in request.POST:
        Contact.new_contact(request.POST)
    if 'btn_new_list' in request.POST:
        groups = request.POST.getlist('groups[]')
        List.create(name=request.POST['name_list'],
                            description=request.POST['desc_list'],
                            created_by=request.user,
                            groups=groups)

    return render(request,
                  'contacts/lists.html',
                  {'lists': lists,
                   'inactive_lists': inactive_lists,
                   'inactive_contacts': inactive_contacts,
                   "user": request.user,
                   "countries": countries,
                   "cities": cities,
                   "zip_codes": zip_codes,
                   "states": states,
                   "announcements": announcements,
                   "conversations": conversations,
                   "chaters": users,
                   "errors": errors})


def contacts_lists_details(request, list):
    announcements = Announcement.objects.all()
    users = User.objects.exclude(username=request.user.username)
    conversations = Conversation.objects.filter(users=request.user).order_by('-date_last_message')
    l = List.objects.get(pk=list)

    if 'btn_delcontact' in request.POST:
        Contact.objects.get(pk=request.POST['contact']).delete()

    return render(request, 'contacts/list_details.html', {'list': l,
                                                          "announcements": announcements,
                                                          "conversations": conversations,
                                                          "user": request.user,
                                                          "chaters": users})


def contacts_details(request, list, contact):
    announcements = Announcement.objects.all()
    users = User.objects.exclude(username=request.user.username)
    conversations = Conversation.objects.filter(users=request.user).order_by('-date_last_message')

    c = Contact.objects.get(pk=contact)
    if 'btn_newnote' in request.POST:
        Note.objects.create(description=request.POST['newnote'],
                            author=request.user,
                            contact=c)
    url_profile_picture = FileManager.get_profile_picture(request.user)
    return render(request, 'contacts/contact_details.html', {'contact': c,
                                                             "announcements": announcements,
                                                             "conversations": conversations,
                                                             "user": request.user,
                                                             "chaters": users,
                                                             "url_profile_picture": url_profile_picture})