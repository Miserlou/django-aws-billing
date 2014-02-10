from django.db import models

# Example:
#
# {'AvailabilityZone': '',
#  'Cost': '0.00000120',
#  'InvoiceID': 'Estimated',
#  'ItemDescription': '$0.004 per 10,000 GET and all other requests',
#  'LinkedAccountId': '572107770384',
#  'Operation': 'ReadACL',
#  'PayerAccountId': '572107770384',
#  'PricingPlanId': '349114',
#  'ProductName': 'Amazon Simple Storage Service',
#  'Rate': '0.0000004000',
#  'RateId': '2016509',
#  'RecordId': '16550049848010735519421357', 
#  'RecordType': 'LineItem',
#  'ReservedInstance': 'N',
#  'ResourceId': 'aws-billing-info-bucket',
#  'SubscriptionId': '46364503',
#  'UsageEndDate': '2014-02-03 13:00:00',
#  'UsageQuantity': '3.00000000',
#  'UsageStartDate': '2014-02-03 12:00:00',
#  'UsageType': 'USW2-Requests-Tier2'}

class BillingRecord(models.Model):

    availablility_zone = models.CharField('Availability Zone', null=True, blank=True, max_length=255)
    cost = models.FloatField('Cost', null=True, blank=True)
    invoice_id = models.CharField('Invoice ID', null=True, blank=True, max_length=255)
    item_description = models.CharField('Item Description', null=True, blank=True, max_length=255)
    linked_account_id = models.IntegerField('Linked Account ID', null=True, blank=True)
    operation = models.CharField('Read ACL', null=True, blank=True, max_length=255)
    payer_account_id = models.IntegerField('Payer Account ID', null=True, blank=True)
    pricing_plan_id = models.IntegerField('Pricing Plan ID', null=True, blank=True)
    product_name = models.CharField('Product Name', null=True, blank=True, max_length=255)
    rate = models.FloatField('Rate', null=True, blank=True)
    rate_id = models.IntegerField('Rate ID', null=True, blank=True)
    record_id = models.CharField('Record ID', null=False, blank=False, unique=True, max_length=255) # This is the magic
    record_type = models.CharField('Record Type', null=True, blank=True, max_length=255)
    reserved_instance = models.CharField('Reserved Instance', null=True, blank=True, max_length=255)
    resource_id = models.CharField('Resource ID', null=True, blank=True, max_length=255)
    subscription_id = models.IntegerField('Subscription ID', null=True, blank=True)
    usage_end_date = models.DateTimeField('Usage End Date', null=True, blank=True)
    usage_quantity = models.FloatField('Usage Quantity', null=True, blank=True)
    usage_start_date = models.DateTimeField('Usage Start Date', null=True, blank=True)
    usage_type = models.CharField('Usage Type', null=True, blank=True, max_length=255)

    def __unicode__(self):
        return "BillingRecord: " + str(self.record_id) + " " + str(self.resource_id)

    def save(self):

        super(BillingRecord, self).save()
        return True