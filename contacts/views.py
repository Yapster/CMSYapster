from django.shortcuts import render
from contacts.models import Note, List, Contact
from admins.models import CmsUser

def contacts_lists(request):
    lists = List.objects.filter(is_active=True)
    inactive_lists = List.objects.filter(is_active=False)
    inactive_contacts = Contact.objects.filter(is_active=False)
    if 'btn_delgroup' in request.POST:
        l = List.objects.get(name=request.POST['list'])
        l.delete()
    if 'btn_active' in request.POST:
        l = List.objects.get(name=request.POST['list'])
    return render(request,
                  'contacts/lists.html',
                  {'lists': lists,
                   'inactive_lists': inactive_lists,
                   'inactive_contacts': inactive_contacts})


def contacts_lists_details(request, list):
    l = List.objects.get(pk=list)
    return render(request, 'contacts/list_details.html', {'list': l})


def contacts_details(request, list, contact):
    c = Contact.objects.get(pk=contact)
    if 'btn_newnote' in request.POST:
        Note.objects.create(description=request.POST['newnote'],
                            author=request.user,
                            contact=c)
    return render(request, 'contacts/contact_details.html', {'contact': c})