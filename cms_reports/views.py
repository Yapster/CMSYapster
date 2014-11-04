from django.core.context_processors import request
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from report.models import Report
from cms_reports.models import CmsReport, TypeReport, ReportNote
from scripts import *


def reports(request):
    reports = Report.objects.filter(is_active=True).order_by('-datetime_reported')
    inactive_reports = Report.objects.filter(is_active=False).order_by('-datetime_reported')
    cms_reports = {}
    all_reports = Report.objects.all().order_by('-datetime_reported')
    for report in all_reports:
        cms_report = CmsReport.objects.filter(report_id=report.report_id).exists()
        if cms_report:
            cms_reports[report.report_id] = CmsReport.objects.get(report_id=report.report_id)


    return render(request,
                  "reports/reports.html",
                  {"reports": reports,
                   "inactive_reports": inactive_reports,
                   "cms_reports": cms_reports,
                   "u": request.user})


@csrf_exempt
def post_actions(request):
    if request.POST:
        if request.POST['typePost'] == 'take_in_charge':
            CmsReport.objects.create(report_id=request.POST['reportId'],
                                     user_in_charge=User.objects.get(pk=request.user.id))
        if request.POST['typePost'] == 'checked':
            r = Report.objects.get(pk=request.POST['reportId'])
            r.is_active = False
            r.save()
        elif request.POST['typePost'] == 'unchecked':
            r = Report.objects.get(pk=request.POST['reportId'])
            r.is_active = True
            r.save()
    return render(request,
                  "reports/in_charge.html",
                  {"u": request.user})


@csrf_exempt
def report(request, report_id):
    r = Report.objects.get(pk=report_id)
    try:
        r_cms = CmsReport.objects.get(report_id=r.report_id)
    except:
        r_cms = None
    u = User.objects.using('ye_1_db_1').get(pk=r.user_id)
    if request.POST:
        if 'new_note_button' in request.POST:
            ReportNote.objects.create(owner=request.user,
                                      report=r_cms,
                                      text=request.POST['new_note_text'])
        if 'new_answer_button' in request.POST:
            print("Email Reply")

    return render(request,
                  "listings/report.html",
                  {"r": r,
                   "r_cms": r_cms,
                   "u": u,
                   "current_u": request.user})