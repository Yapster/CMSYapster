from django import template
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template.response import SimpleTemplateResponse
from files_manager.models import FileManager
from django.template.loader import render_to_string
from tools.tools import *

register = template.Library()

@register.filter(name='get_first')
def get_first(c):
    try:
        return c[0]
    except KeyError:
        return ''

@register.filter(name='get_second')
def get_second(c):
    try:
        return c[1]
    except KeyError:
        return ''

@register.filter(name='get_key')
def get_key(d):
    try:
        for key in d.keys():
            return key
    except KeyError:
        return ''

@register.filter(name='get_value')
def get_value(d):
    try:
        for val in d.values():
            return val
    except KeyError:
        return ''

@register.filter(name='access')
def access(value, arg):
    try:
        return value[arg]
    except KeyError:
        return ''

@register.filter(name='get_type_list')
def get_type_list(list):
    if list:
        return list[0].__class__.__name__
    return ""


@register.filter(name='get_type_list_from_dic')
def get_type_list_from_dic(dic):
    if dic:
        return dic[1][0].__class__.__name__
    return

@register.filter(name='get_profile_pic')
def get_profile_pic(userId):
    if userId:
        u = User.objects.get(pk=userId)
        return FileManager.get_profile_picture(u)

@register.filter(name='get_url_yapsterapp_s3')
def get_url_yapsterapp_s3(path):
    if path:
        b = boto_init_s3('yapsterapp')
        if b:
            try:
                return b.get_key(path).generate_url(expires_in=600)
            except:
                return ""
        return ""

@register.filter(name='get_apps_list')
def get_apps_list(list):
    l = []
    if list:
        for p in list:
            if p.content_type.app_label not in l:
                l.append(p.content_type.app_label)
    return l

@register.filter(name='get_user_info')
def get_user_info(user_id):
    u = User.objects.using('ye_1_db_1').get(pk=user_id)
    info = {}
    info['username'] = u.username

    return info


@register.filter(name='get_username')
def get_username(user_id):
    u = User.objects.using('ye_1_db_1').get(pk=user_id)

    return u.username

@register.filter(name='cms_report_get_username')
def cms_report_get_username(dic, value):
    try:
        return dic[value].user_in_charge
    except:
        return ''

@register.filter(name='user_window')
def user_window(user_id):
    u = User.objects.using('ye_1_db_1').get(pk=user_id)
    return render_to_string("listings/user.html", {"u": u})