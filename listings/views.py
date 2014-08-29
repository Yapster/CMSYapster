from django.shortcuts import render
from django.contrib.auth.models import User
from location.models import Country
from django.views.decorators.csrf import csrf_exempt
from yap.models import Hashtag, Yap


@csrf_exempt
def list_users(request):
    users = []
    if request.POST:
        l = request.POST.getlist('users[]')
        for u in l:
            users.append(User.objects.using('ye_1_db_1').get(username=u))

    return render(request,
                  "listings/users.html",
                  {"users": users,
                   "title": request.POST['title']})

@csrf_exempt
def user_details(request):
    u = None
    if request.POST:
        u = User.objects.using('ye_1_db_1').get(username=request.POST['username'])
    return render(request,
                  "listings/user_details.html",
                  {"u": u})

@csrf_exempt
def list_countries(request):
    res = []
    if request.POST:
        l = request.POST.getlist('countries[]')
        if request.POST['title'] == 'Top Countries Users':
            for s in l:
                name, num = s.replace('(', "").replace(")", "").replace("'", "").replace("u", "").split(', ')
                name = name.encode('ascii', 'replace')
                c = Country.objects.using('ye_1_db_1').get(country_name=name)
                res.append((c, num))
    return render(request,
                  "listings/countries.html",
                  {"res": res,
                   "title": request.POST['title']})


@csrf_exempt
def list_hashtags(request):
    hashtags = []
    if request.POST:
        l = request.POST.getlist('hashtags[]')
        for h in l:
            hashtags.append(Hashtag.objects.using('ye_1_db_1').get(hashtag_name=h))

    return render(request,
                  "listings/hashtags.html",
                  {"hashtags": hashtags,
                   "title": request.POST['title']})


@csrf_exempt
def list_yaps(request):
    yaps = []
    if request.POST:
        l = request.POST.getlist('yaps[]')
        for y in l:
            yaps.append(Yap.objects.using('ye_1_db_1').get(title=y))

    return render(request,
                  "listings/yaps.html",
                  {"yaps": yaps,
                   "title": request.POST['title']})