from django.shortcuts import render_to_response, HttpResponse, render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from admins.models import Announcement
from stats.models import Hashtag, Group

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