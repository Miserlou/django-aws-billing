import zipfile
import os.path
import csv

from collections import defaultdict
from boto import connect_s3
from datetime import datetime

'''
This code is originally by ediemert, from here: https://github.com/oddskool/aws_billing

Smushed into a single file and Djangoified by Rich Jones.

'''

# TODO: Cloudfront / STS / SES
services = {
                'Amazon Simple Storage Service':{'name':'s3'},
                'Amazon Elastic Compute Cloud':{'name':'ec2'},
                'Amazon Route 53':{'name':'r53'},
                'Amazon Simple Notification Service':{'name':'sns'},
                'Amazon Simple Queue Service':{'name':'sqs'},
                'Amazon DynamoDB':{'name':'ddb'},
                'Amazon RDS Service':{'name':'rds'},
                'Amazon Virtual Private Cloud':{'name':'vpc'},
                'Amazon SimpleDB':{'name':'sdb'},
                'Amazon ElastiCache':{'name':'eca'},
                'AWS Data Pipeline':{'name':'adp'},
                'Amazon Elastic MapReduce':{'name':'emr'},
                'Amazon Glacier':{'name':'agl'},
                'AWS Support (Developer)':{'name':'sup'},
                '':{'name':'tva'}
            }

def service_name(product_name):
    return services[product_name]['name']

def add_type(d):
    if d['RecordType'] != 'LineItem':
        return None
    for field in ('Cost', 'UsageQuantity'):
        d[field] = float(d[field] if len(d[field]) else 1)
    for field in ('LinkedAccountId', 'InvoiceID', 'RecordType', 'RecordId',
                  'PayerAccountId', 'SubscriptionId'):
        del d[field]
    return d

def forge_key(d):
    service = service_name(d['ProductName'])
    resource_tag = d.get('user:BILLING', None)
    yield 'Total * Total'
    if resource_tag:
        yield ' * '.join(("BILLING", resource_tag))
    else:
        if d["ItemDescription"] == 'Tax of type VAT':
            yield "tva"
        else:
            yield ' * '.join(("BILLING", 'untagged'))
    #if not resource_tag:
    if service == 'ec2':
        resource_tag = d['UsageType'].split(':')[0]
        if '-' in resource_tag:
            resource_tag = resource_tag.split('-')[1]
    else:
        resource_tag = d['ResourceId']
    if not d["ItemDescription"] == 'Tax of type VAT':
        yield ' * '.join((service,
                          resource_tag))

def parse_line(stats, d):
    d = add_type(d)
    if not d:
        return
    for key in forge_key(d):
        stats[key]['Cost'] += d['Cost']
        stats[key]['UsageQuantity'] += d['UsageQuantity']

def parse(fd, price_floor_dollars=0.1):
    reader = csv.reader(fd, delimiter=',', quotechar='"')
    legend = None
    stats = defaultdict(lambda: defaultdict(int))
    for i, row in enumerate(reader):
        if not legend:
            legend = row
            continue
        d = dict(zip(legend, row))
        try:
            parse_line(stats, d)
        except Exception as e:
            print "Exception:", type(e), e
            print d
        if i and not i % 10000:
            print i,"lines..."
    stats = [ (resource, cost_usage) for resource, cost_usage in 
                stats.iteritems() if cost_usage['Cost'] > price_floor_dollars ]
    stats.sort(key=lambda x:x[-1]['Cost'], reverse=True)
    return stats


def retrieve_fd(account, bucket_name, month=None, tmp_dir='.'):
    month = month or datetime.now().strftime('%Y-%m')
    fn = "%s-aws-billing-detailed-line-items-with-resources-and-tags-%s.csv" % (account, month)
    remote_fn = "s3://%s/%s.zip" % (bucket_name, fn)
    print "remote fn:", remote_fn
    s3 = connect_s3()
    bucket = s3.get_bucket(bucket_name)
    key = bucket.get_key(fn+'.zip')
    if not key:
        raise Exception("remote file not ready : %s" % remote_fn)
    key.get_contents_to_filename(os.path.join(tmp_dir, fn+'.zip'))
    return zipfile.ZipFile(os.path.join(tmp_dir, fn+'.zip')).open(fn)

# Utility
unit_transforms = { 
    'ByteHrs':{'transform':lambda x: x,
               'unit':'GB'},
    'Requests':{'transform':lambda x:x,
                'unit':'requests'},
    'BoxUsage':{'transform':lambda x:int(x),
                'unit':'hours'},
    'VolumeUsage':{'transform':lambda x:int(x),
                   'unit':'GB'},
    'VolumeP-IOPS.piops':{'transform':lambda x:int(x),
                          'unit':'GB'},
    'LoadBalancerUsage':{'transform':lambda x:int(x),
                          'unit':'hours'},
    'DataTransfer':{'transform':lambda x:x/(1024**3),
                    'unit':'GB'},
    'DNS-Queries':{'transform':lambda x:x/(1024**3),
                    'unit':'requests'},
    'ReadCapacityUnit-Hrs':{'transform':lambda x:int(x),
                          'unit':'hours'},
                   }

def unitize(usage_type, usage_quantity):
    for unit, unit_data in unit_transforms.iteritems():
        if unit in usage_type:
            s = "%.2f %s"%(unit_data['transform'](usage_quantity),
                           unit_data['unit'])
            return s
    #print "XOXOX","unknown usage type: <%s>"%usage_type
    return "%f (unknown unit)"%usage_quantity

# Demo
def parse_all(account_id, bucket_name):
    fd = retrieve_fd(account_id, bucket_name)
    stats = parse(fd)
    self.application.read_time = now
    for d in stats:
        if 'BILLING' in d[0]:
            print "%s %.2f" % (d[0][10:],d[1]['Cost']))
