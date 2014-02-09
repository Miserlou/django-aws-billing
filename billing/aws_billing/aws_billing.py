from django.db.models import Sum
from .models import BillingRecord

def get_cost_for_resource(resource_id):
    try:
        cost = BillingRecord.objects.filter(resource_id=resource_id).aggregate(Sum('cost'))['cost__sum']
        return cost
    except Exception, e:
        print e
        return -1

def get_total_cost():
    try:
        cost = BillingRecord.objects.all().aggregate(Sum('cost'))['cost__sum']
        return cost
    except Exception, e:
        print e
        return -1