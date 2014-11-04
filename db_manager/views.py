from _csv import list_dialects
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import boto.rds
import boto.ec2
import boto.ec2.cloudwatch
import datetime
from django.views.decorators.csrf import csrf_exempt
import collections

@login_required(login_url='/login/')
def home_database(request):
    conn = boto.rds.connect_to_region("us-east-1")
    cw = boto.ec2.cloudwatch.connect_to_region("us-east-1")
    instances = conn.get_all_dbinstances()
    rds_hosts = {}
    rds_ports = {}
    list_metrics = None
    for instance in instances:
        endpoint = instance.endpoint
        list_metrics = cw.list_metrics(dimensions={'DBInstanceIdentifier':[instance.id]},namespace="AWS/RDS")
        list_metrics.sort(key=lambda r:r.name)
        rds_hosts[instance.id] = endpoint[0]
        rds_ports[instance.id] = endpoint[1]

    return render(request,
                  'db_manager/rds_home.html',
                  {"instances": instances,
                   "rds_hosts": rds_hosts,
                   "rds_ports": rds_ports,
                   "list_metrics": list_metrics})


@login_required(login_url='/login/')
def home_server(request):
    conn2 = boto.ec2.connect_to_region("us-east-1")
    ec2reservations = conn2.get_all_instances()
    cw = boto.ec2.cloudwatch.connect_to_region("us-east-1")
    ec2instances = []
    list_metrics = None
    for reservation in ec2reservations:
        for instance in reservation.instances:
            list_metrics = cw.list_metrics(dimensions={'InstanceId':[instance.id]},namespace="AWS/EC2")
            list_metrics.sort(key=lambda r:r.name)
            ec2instances.append(instance)

    return render(request,
                  'db_manager/ec2_home.html',
                  {"ec2instances": ec2instances,
                   "list_metrics": list_metrics})


@login_required(login_url='/login/')
def rds_details(request, instance):
    cw = boto.ec2.cloudwatch.connect_to_region("us-east-1")
    list_metrics = cw.list_metrics(dimensions={'DBInstanceIdentifier':[instance]},namespace="AWS/RDS")
    list_metrics.sort(key=lambda r:r.name)
    return render(request,
                  'db_manager/rds_details.html',
                  {"instance": instance,
                   "list_metrics": list_metrics})


def ec2_details(request, instance):
    cw = boto.ec2.cloudwatch.connect_to_region("us-east-1")
    list_metrics = cw.list_metrics(dimensions={'InstanceId':[instance]},namespace="AWS/EC2")
    list_metrics.sort(key=lambda r:r.name)
    return render(request,
                  'db_manager/ec2_details.html',
                  {"instance": instance,
                   "list_metrics": list_metrics})


@csrf_exempt
@login_required(login_url='/login/')
def graphs_rds(request):
    if 'instances[]' in request.POST:
        l_instances = request.POST.getlist('instances[]')
        cw = boto.ec2.cloudwatch.connect_to_region("us-east-1")
        dic = collections.OrderedDict()
        first = True
        unit = "Unknown"
        for instance in l_instances:
            metric = cw.list_metrics(metric_name=request.POST['type_search'], dimensions={'DBInstanceIdentifier':[instance]},namespace="AWS/RDS")[0]
            data = metric.query(datetime.datetime.utcnow() - datetime.timedelta(minutes=int(request.POST['type_time'])),
                                datetime.datetime.utcnow(),
                                request.POST['type_stats'],
                                period=int(request.POST['type_period']))
            data.sort(key=lambda r:r['Timestamp'])
            if first:
                unit = data[0]['Unit']
                for i in data:
                    date = i['Timestamp'].isoformat().replace("T", " ")
                    dic[date] = str(i[request.POST['type_stats']])
                first = False
            else:
                for i in data:
                    date = i['Timestamp'].isoformat().replace("T", " ")
                    try:
                        dic[date] = dic[date] + ', ' + str(i[request.POST['type_stats']])
                    except KeyError:
                        continue

        return render(request,
                  'db_manager/multiple_graphs.html',
                  {"dic": dic.items(),
                   "l_instances": l_instances,
                   "unit": unit,
                   "type_search": request.POST['type_search']})
    return

@login_required(login_url='/login/')
@csrf_exempt
def display_one_graph_rds(request):
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
                       "type_search": request.POST['type_search'],
                       "instance_id": request.POST['instance']})

@login_required(login_url='/login/')
@csrf_exempt
def graph_ec2(request):
    if 'time_graph' in request.POST:
        # Get Metric from AWS
        cw = boto.ec2.cloudwatch.connect_to_region("us-east-1")
        metric = cw.list_metrics(metric_name=request.POST['type_search'], dimensions={'InstanceId':[request.POST['instance']]},namespace="AWS/EC2")[0]
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
                       "type_search": request.POST['type_search'],
                       "instance_id": request.POST['instance']})

@login_required(login_url='/login/')
@csrf_exempt
def graphs_ec2(request):
    if 'instances[]' in request.POST:
        l_instances = request.POST.getlist('instances[]')
        cw = boto.ec2.cloudwatch.connect_to_region("us-east-1")
        dic = collections.OrderedDict()
        first = True
        unit = "Unknown"
        for instance in l_instances:
            metric = cw.list_metrics(metric_name=request.POST['type_search'], dimensions={'InstanceId':[instance]},namespace="AWS/EC2")[0]
            data = metric.query(datetime.datetime.utcnow() - datetime.timedelta(minutes=int(request.POST['type_time'])),
                                datetime.datetime.utcnow(),
                                request.POST['type_stats'],
                                period=int(request.POST['type_period']))
            data.sort(key=lambda r:r['Timestamp'])
            if first:
                unit = data[0]['Unit']
                for i in data:
                    date = i['Timestamp'].isoformat().replace("T", " ")
                    dic[date] = str(i[request.POST['type_stats']])
                first = False
            else:
                for i in data:
                    date = i['Timestamp'].isoformat().replace("T", " ")
                    try:
                        dic[date] = dic[date] + ', ' + str(i[request.POST['type_stats']])
                    except KeyError:
                        #print(date, str(i[request.POST['type_stats']]))
                        continue

        return render(request,
                  'db_manager/multiple_graphs.html',
                  {"dic": dic.items(),
                   "l_instances": l_instances,
                   "unit": unit,
                   "type_search": request.POST['type_search']})
    return