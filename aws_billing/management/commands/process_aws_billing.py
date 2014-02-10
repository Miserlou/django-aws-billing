from django.core.management.base import BaseCommand, CommandError
from django.conf import settings as aws_settings

try:
    from libs.django_aws_billing.aws_billing.models import BillingRecord
except Exception, e:
    from aws_billing.models import BillingRecord

import time
import sys
import csv
import os
import zipfile

from datetime import datetime
from pprint import pprint
from collections import defaultdict
from boto import connect_s3

class Command(BaseCommand):
    args = '<filename>'
    help = 'Parse an AWS Billing CSV into aws_billing format.'

    def handle(self, *args, **options):

        filename = None
        for arg in args:
            filename = arg
            fd = open(filename)
        if not filename:
            fd = retrieve_remote_stats(aws_settings.AWS_ACCOUNT_ID.replace('-', ''), aws_settings.AWS_BILLING_BUCKET)

        reader = csv.reader(fd, delimiter=',', quotechar='"')
        legend = None
        stats = defaultdict(lambda: defaultdict(int))

        for row in reader:

            # First, get the legend from the very first row.
            if not legend:
                legend = row    
                continue

            # Parse the row into a Python dict using the legend.
            data = dict(zip(legend, row))
            record_id = data['RecordId']

            # This is a summary record, not a billing record.
            if not record_id:
                continue

            if BillingRecord.objects.filter(record_id=record_id).exists():
                continue
            else:
                # Here we go!
                record = BillingRecord()
                record.availablility_zone = data['AvailabilityZone']
                record.cost = data['Cost']
                record.invoice_id = data['InvoiceID']
                record.item_description = data['ItemDescription']
                record.linked_account_id = data['LinkedAccountId']
                record.operation = data['Operation']
                record.payer_account_id = data['PayerAccountId']
                record.pricing_plan_id = data['PricingPlanId']
                record.product_name = data['ProductName']
                record.rate = data['Rate']
                record.rate_id = data['RateId']
                record.record_id = data['RecordId'] # This is the magic
                record.record_type = data['RecordType']
                record.reserved_instance = data['ReservedInstance']
                record.resource_id = data['ResourceId']
                record.subscription_id = data['SubscriptionId']
                record.usage_end_date = data['UsageEndDate']
                record.usage_quantity = data['UsageQuantity']
                record.usage_start_date= data['UsageStartDate']
                record.usage_type = data['UsageType']
                record.save()

def retrieve_remote_stats(account, bucket_name, month=None, tmp_dir='.'):
    month = month or datetime.now().strftime('%Y-%m')
    fn = "%s-aws-billing-detailed-line-items-with-resources-and-tags-%s.csv" % (account, month)
    remote_fn = "s3://%s/%s.zip" % (bucket_name, fn)
    s3 = connect_s3(aws_settings.AWS_ACCESS_KEY, aws_settings.AWS_SECRET_ACCESS_KEY)
    bucket = s3.get_bucket(bucket_name)
    key = bucket.get_key(fn+'.zip')
    if not key:
        raise Exception("remote file not ready : %s" % remote_fn)
    key.get_contents_to_filename(os.path.join(tmp_dir, fn+'.zip'))
    return zipfile.ZipFile(os.path.join(tmp_dir, fn+'.zip')).open(fn)

