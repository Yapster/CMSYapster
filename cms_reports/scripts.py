from cms_reports.models import CmsReport


def import_reports(reports, cms_reports):
    """
    Import Reports to CmsReports
    """

    for report in reports:
        if not CmsReport.objects.filter(report_id=report.report_id).exists():

            CmsReport.objects.create()
    return