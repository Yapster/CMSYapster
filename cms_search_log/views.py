from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from cms_location.models import *

@csrf_exempt
def form_fields(request):
    if 'type_search' in request.POST:
        if request.POST['type_search'] == "1":
            countries = CmsCountry.objects.all()
            cities = CmsCity.objects.all()
            states = CmsUSState.objects.all()
            return render(request, "search/form_users.html", {"countries": countries,
                                                              "cities": cities,
                                                              "states": states})
        if request.POST['type_search'] == "2":
            return render(request, "search/form_yaps.html", {})
        if request.POST['type_search'] == "3":
            return render(request, "search/form_reyaps.html", {})
        if request.POST['type_search'] == "4":
            return render(request, "search/form_likes.html", {})
        if request.POST['type_search'] == "5":
            return render(request, "search/form_listens.html", {})
        if request.POST['type_search'] == "6":
            return render(request, "search/form_channels.html", {})
        if request.POST['type_search'] == "7":
            return render(request, "search/form_hashtags.html", {})
        if request.POST['type_search'] == "8":
            return render(request, "search/form_reports.html", {})
    return

@csrf_exempt
def results(request):
    if 'form' in request.POST:
        def get_params(s_params):
            l = s_params.split("&")
            dict = {}
            for x in l:
                sub_l = x.split("=")
                if sub_l[1]:
                    dict[sub_l[0]] = sub_l[1]
            return dict
        kwargs = get_params(request.POST['form'])
        print(kwargs)
    return