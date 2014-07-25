from django.shortcuts import render
import boto.rds
import boto.ec2
import boto.ec2.cloudwatch
import datetime
from django.views.decorators.csrf import csrf_exempt
import collections

def home_database(request):
    conn = boto.rds.connect_to_region("us-east-1")
    instances = conn.get_all_dbinstances()
    conn2 = boto.ec2.connect_to_region("us-east-1")
    ec2reservations = conn2.get_all_instances()
    ec2instances = []
    for reservation in ec2reservations:
        for instance in reservation.instances:
            ec2instances.append(instance)

    return render(request,
                  'db_manager/home.html',
                  {"instances": instances,
                   "ec2instances": ec2instances})


def rds_details(request, instance):
    cw = boto.ec2.cloudwatch.connect_to_region("us-east-1")
    list_metrics = cw.list_metrics(dimensions={'DBInstanceIdentifier':[instance]},namespace="AWS/RDS")

    return render(request,
                  'db_manager/rds_details.html',
                  {"instance": instance,
                   "list_metrics": list_metrics})


def ec2_details(request, instance):
    cw = boto.ec2.cloudwatch.connect_to_region("us-east-1")
    # metric = cw.get_metric_statistics(300,
    #                                   datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
    #                                   datetime.datetime.utcnow(),
    #                                   'CPUUtilization',
    #                                   'AWS/EC2',
    #                                   'Average',
    #                                   dimensions={'InstanceId':[instance]})
    return render(request,
                  'db_manager/ec2_details.html',
        {})

@csrf_exempt
def graph_rds(request):
    if 'time_graph' in request.POST:
        # Get Metric from AWS
        cw = boto.ec2.cloudwatch.connect_to_region("us-east-1")
        metric = cw.list_metrics(metric_name=request.POST['type_search'], dimensions={'DBInstanceIdentifier':[request.POST['instance']]},namespace="AWS/RDS")[0]
        data = metric.query(datetime.datetime.utcnow() - datetime.timedelta(minutes=int(request.POST['type_time'])),
                            datetime.datetime.utcnow(),
                            request.POST['type_stats'],
                            period=int(request.POST['type_period']))
        # Sorted by Date + Convert Date into String
        unit = data[0]['Unit']
        data.sort(key=lambda r:r['Timestamp'])
        dic = collections.OrderedDict()
        for i in data:
            date = i['Timestamp'].isoformat().replace("T", " ")
            dic[date] = i[request.POST['type_stats']]


        return render(request,
                      'db_manager/graph_displaying.html',
                      {"dic": dic.items(),
                       "unit": unit,
                       "type_search": request.POST['type_search']})