#!/usr/bin/env python

import signalfx
import logging
import sys
import time
import random


if __name__ == '__main__':
    client = signalfx.SignalFx()
    ingest = client.ingest('XXXX')
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    try:
        while True:
            ingest.send(gauges=[
                {
                    'metric': 'metric_name',
                    'value': random.randint(1, 10),
                    'dimensions': {'name': 'testing',
                        'env': 'sandbox',
                        'aws_region': 'us-east-1'},
                    }])
            time.sleep(10)
    except KeyboardInterrupt:
        pass
