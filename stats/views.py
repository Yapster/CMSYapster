from django.shortcuts import render_to_response, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def homepage(request):
    """
    Display general stats
    """
    return render_to_response('stats/home.html',
                            {},
                            content_type=RequestContext(request))

def stats(request):
    return render_to_response('stats/statistics.html',
        {},
                              content_type=RequestContext(request))

def search(request):
    """
    Display research view
    """
    return render_to_response('stats/index.html',
                            {},
                            content_type=RequestContext(request))

def hashtag(request, tag):
    """
    Display hashtag with count of people that used it and few yaps
    """
    return HttpResponse("TODO")

def group_page(request, group):
    """
    Display group page with count people in it and few yaps
    """
    return HttpResponse("TODO")