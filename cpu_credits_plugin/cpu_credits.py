import collectd
import boto3
import datetime
import requests


def get_cloudwatch_metric(instance, metric, region):
    cloudwatch = boto3.client('cloudwatch', region_name=region)
    start = datetime.datetime.utcnow() - datetime.timedelta(minutes=60)
    end = datetime.datetime.utcnow()
    data = cloudwatch.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName=metric,
        Dimensions=[{'Name': 'InstanceId', 'Value': instance}],
        StartTime=start,
        EndTime=end,
        Period=300,
        Statistics=['Sum']
    )
    datapoints = data['Datapoints']
    count = 0
    total = 0
    for d in datapoints:
        total = total + d['Sum']
        count = count + 1
    if total > 0:
        avg = (total / count)
        return avg
    return 0


def get_instance_details():
    instance_id = requests.get('http://169.254.169.254/latest/meta-data/instance-id')
    instance_type = requests.get('http://169.254.169.254/latest/meta-data/instance-type')
    instance_region = requests.get('http://169.254.169.254/latest/meta-data/placement/availability-zone')
    instance_region = instance_region.text[:-1]
    return instance_id.text, instance_type.text, instance_region


def collectd_dispatch(plugin_name, plugin_host, plugin_type, plugin_values, plugin_interval=300):
    collectd.info('cpu_credits:' + plugin_type + ' -> ' + str(plugin_values))
    metric = collectd.Values()
    metric.plugin = plugin_name
    metric.host = plugin_host
    metric.interval = plugin_interval
    metric.type = plugin_type
    metric.values = [plugin_values]
    metric.dispatch()


def collectd_send_metrics():
    iid, itype, iregion = get_instance_details()
    collectd.info('cpu_credits: instance type is ' + itype )
    collectd.info('cpu_credits: instance id ' + iid)
    if itype.split('.')[0] == "t2":
        balance = get_cloudwatch_metric(iid, 'CPUCreditBalance', iregion)
        usage = get_cloudwatch_metric(iid, 'CPUCreditUsage', iregion)
        collectd_dispatch('cpu_metrics', iid, 'cpu_credit_balance', balance)
        collectd_dispatch('cpu_metrics', iid, 'cpu_credit_usage', usage)


def collectd_conf():
    collectd.debug('conf stage')


def collectd_init():
    collectd.debug('init stage')


collectd.register_config(collectd_conf)
collectd.register_init(collectd_init)
collectd.register_read(collectd_send_metrics)
