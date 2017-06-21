# CPU CREDITS PLUGIN
If you need to get cpu credits from EC2 but do not wish to use the signalFX ec2 metrics
you can use this plugin instead

### Requirements

#### Python Modules
Install the following modules ( use pip-2.6 since signalFX collectd uses that for python modules )
- requests
- collectd
- boto3

### IAM roles
you will need IAM access to query cloudwatch
```
        {
            "Sid": "CloudWatchMetrics",
            "Effect": "Allow",
            "Action": [
                "cloudwatch:ListMetrics",
                "cloudwatch:GetMetricStatistics",
                "cloudwatch:GetMetricData"
            ],
            "Resource": "*"
        }
```

### Install
- copy `cpu_credits.py` and `cpu-credits-types.db` to `/usr/share/collectd/cpu-credits-plugin`
- place `cpu-credits.conf` in `/etc/collectd.d/managed_config`
- reload collectd


