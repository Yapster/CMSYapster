from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login


def login_user(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        current_user = authenticate(username=username, password=password)
        if current_user is not None:
            if current_user.is_active:
                login(request, current_user)
                return HttpResponseRedirect('/home/')
    return render_to_response('auths/login.html',
                            {},
                                context_instance=RequestContext(request))

def homepage(request):
    return render_to_response('stats/home.html',
                            {},
                              content_type=RequestContext(request))