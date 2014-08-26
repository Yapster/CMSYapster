from django.shortcuts import render
from files_manager.models import FileForm, FileManager
from yap.models import *
import boto

def channel(request, id):
    c = boto.connect_s3()
    b = c.get_bucket('yapsterapp')
    if 'button_new_pic' in request.POST:
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['new_pic']
            path_bucket = "yapsterchannels/" + request.POST['channel_name'] + request.POST['type_pix'] + ".png"
            FileManager.store("yapsterapp", path_bucket.lower(), file.read(), file_type="channel")

    channel = Channel.objects.get(pk=id)
    l_yaps = Yap.objects.filter(channel=channel).order_by('-date_created')[:5]
    d_urls = {}

    if b:
        path_icon_explore_path_clicked = b.get_key(channel.icon_explore_path_clicked)
        path_icon_explore_path_unclicked = b.get_key(channel.icon_explore_path_unclicked)
        path_icon_yap_path_clicked = b.get_key(channel.icon_yap_path_clicked)
        path_icon_yap_path_unclicked = b.get_key(channel.icon_yap_path_unclicked)
        d_urls['icon_explore_path_clicked'] = path_icon_explore_path_clicked.generate_url(expires_in=600)
        d_urls['icon_explore_path_unclicked'] = path_icon_explore_path_unclicked.generate_url(expires_in=600)
        d_urls['icon_yap_path_clicked'] = path_icon_yap_path_clicked.generate_url(expires_in=600)
        d_urls['icon_yap_path_unclicked'] = path_icon_yap_path_unclicked.generate_url(expires_in=600)



    return render(request,
                  "listings/channel.html",
                  { "c": channel,
                    "l_yaps": l_yaps,
                    "d_urls": d_urls})


def new_channel(request):
    if request.POST:
        kwargs = {}


        kwargs['channel_name'] = request.POST['name'].lower().title()
        kwargs['channel_description'] = request.POST['description']
        kwargs['icon_explore_path_clicked'] = "yapsterchannels/" + kwargs['channel_name'] +"/explore/" + kwargs['channel_name'] + "_explore_clicked.png"
        kwargs['icon_explore_path_unclicked'] = "yapsterchannels/" + kwargs['channel_name'] +"/explore/" + kwargs['channel_name'] + "_explore_unclicked.png"
        kwargs['icon_yap_path_clicked'] = "yapsterchannels/" + kwargs['channel_name'] +"/yap/" + kwargs['channel_name'] + "_yap_clicked.png"
        kwargs['icon_yap_path_unclicked'] = "yapsterchannels/" + kwargs['channel_name'] +"/yap/" + kwargs['channel_name'] + "_yap_unclicked.png"
        if 'is_bonus' in request.POST:
            kwargs['is_bonus_channel'] = True
        if 'is_promo' not in request.POST:
            kwargs['is_promoted'] = False

        kwargs_user = {}
        kwargs_user['first_name'] = "Yapster"
        kwargs_user['last_name'] = kwargs['channel_name']
        kwargs_user['username'] = "yapster" + request.POST['name'].lower()
        kwargs_user['email'] = request.POST['name'].lower() + "@yapster.co"
        kwargs_user['email'] = request.POST['name'].lower() + "@yapster.co"
        kwargs_user['email'] = request.POST['name'].lower() + "@yapster.co"



        file = request.FILES['icon_explore_clicked']
        path_bucket = kwargs['icon_explore_path_clicked']
        FileManager.store("yapsterapp", path_bucket.lower(), file.read(), file_type="channel")

        file = request.FILES['icon_explore_unclicked']
        path_bucket = kwargs['icon_explore_path_unclicked']
        FileManager.store("yapsterapp", path_bucket.lower(), file.read(), file_type="channel")

        file = request.FILES['icon_yap_clicked']
        path_bucket = kwargs['icon_yap_path_clicked']
        FileManager.store("yapsterapp", path_bucket.lower(), file.read(), file_type="channel")

        file = request.FILES['icon_yap_unclicked']
        path_bucket = kwargs['icon_yap_path_unclicked']
        FileManager.store("yapsterapp", path_bucket.lower(), file.read(), file_type="channel")

        Channel.objects.create(**kwargs)

    return render(request,
                  "channels/new_channel.html")