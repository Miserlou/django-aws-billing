from django.db.models import Sum
from .models import BillingRecord
import pprint

def get_cost_for_resource(resource_id):
    cost = BillingRecord.objects.filter(resource_id=resource_id).aggregate(Sum('cost'))['cost__sum']
    return cost

def get_total_cost():
    cost = BillingRecord.objects.all().aggregate(Sum('cost'))['cost__sum']
    return cost

def get_all_resources():
    resources = BillingRecord.objects.values('resource_id').distinct()

    resource_list = []
    for resource in resources:
        resource_list.append(resource.values()[0])

    return resource_list

def get_all_costs_by_resource():
    resources = get_all_resources()
    costs = {}

    for resource in resources:
        costs[resource] = get_cost_for_resource(resource)

    return costs