from django.core.management.base import BaseCommand, CommandError
import time

import sys
import csv
from pprint import pprint
from collections import defaultdict

class Command(BaseCommand):
    args = '<filename>'
    help = 'Parse an AWS Billing CSV into aws_billing format.'

    def handle(self, *args, **options):

        for arg in args:
            filename = arg

        fd = open(filename)
        reader = csv.reader(fd, delimiter=',', quotechar='"')
        legend = None
        stats = defaultdict(lambda: defaultdict(int))

        for row in reader:

            # First, get the 
            if not legend:
                legend = row    
                print legend
                continue
            d = dict(zip(legend, row))

            pprint(d)
            print "\n"