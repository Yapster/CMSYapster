from stats.models import *
import datetime
# import cStringIO as StringIO
# import ho.pisa as pisa
# from django.template.loader import get_template
# from django.template import Context
# from django.http import HttpResponse
# from cgi import escape


def get_stat_method(name_method, type_stats):
    """

    :param name_method: String. Name of the method required
    :param type_stats: String. Name of the stats group
    :return:
    """
    global stat_method
    if type_stats == "usership":
        stat_method = getattr(UserManager, name_method)
    elif type_stats == "countries":
        stat_method = getattr(CountryManager, name_method)
    elif type_stats == "hashtags":
        stat_method = getattr(HashtagManager, name_method)
    elif type_stats == "listens":
        stat_method = getattr(ListenManager, name_method)
    elif type_stats == "yaps":
        stat_method = getattr(YapManager, name_method)
    elif type_stats == "likes":
        stat_method = getattr(LikeManager, name_method)
    elif type_stats == "reyaps":
        stat_method = getattr(ReyapManager, name_method)
    return stat_method


def get_time(date, time):
    l_date = date.split('-')
    if not time:
        return
    l_time = time.split(':')
    return datetime.datetime(int(l_date[0]), int(l_date[1]), int(l_date[2]), int(l_time[0]), int(l_time[1]))

# def render_to_pdf(template_src, context_dict):
#     template = get_template(template_src)
#     context = Context(context_dict)
#     html = template.render(context)
#     result = StringIO.StringIO()
#
#     pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))