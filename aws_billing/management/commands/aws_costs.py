from django.core.management.base import BaseCommand
from django.conf import settings as aws_settings

try:
    from libs.django_aws_billing.aws_billing import aws_billing
except Exception, e:
    import aws_billing.aws_billing as aws_billing

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
    help = 'Print AWS Costs.'

    def handle(self, *args, **options):

        all_costs = aws_billing.get_all_costs_by_resource()
        for k, v in all_costs.iteritems():
            print str(k) + ": \t\t\t$" + str(v)

        print "------------------------"
        print "Total cost: \t\t\t$" + str(aws_billing.get_total_cost())
