from django.shortcuts import render_to_response, HttpResponse, render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from admins.models import Announcement

@login_required(login_url='/login/')
def homepage(request):
    """
    Display general stats
    """
    announcements = Announcement.objects.all()

    return render(request, 'stats/home.html', {"announcements": announcements, "user":request.user})


@login_required(login_url='/login/')
def stats(request):
    return render_to_response('stats/statistics.html',
        {},
                              content_type=RequestContext(request))



@login_required(login_url='/login/')
def search(request):
    """
    Display research view
    """
    return render_to_response('stats/index.html',
                            {},
                            content_type=RequestContext(request))


@login_required(login_url='/login/')
def hashtag(request, tag):
    """
    Display hashtag with count of people that used it and few yaps
    """
    return HttpResponse("TODO")


@login_required(login_url='/login/')
def group_page(request, group):
    """
    Display group page with count people in it and few yaps
    """
    return HttpResponse("TODO")