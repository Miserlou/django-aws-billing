![Bezos is a Hustler](http://i.imgur.com/Lw15zkJ.jpg)

django-aws-billing
==================

Django AWS Usage/Billing Package. **Work in Progress**.

* Version: 0.1.0
* Status: Working!
* Not tested in a production setting yet. Should be okay though.

Maps items from CSVs in the AWS programmatic billing access reports to a **BillingRecord** model in Django, allowing billing
queries to be processed via the Django ORM. Also provides some convenience methods to calculate costs for specific
resources. 

## Set up

1. First you need to set up [Programmatic Billing
Access](http://docs.aws.amazon.com/awsaccountbilling/latest/about/programaccess.html) and "detailed billing reporting
with resources and tags" from your [billing preferences
page](https://portal.aws.amazon.com/gp/aws/developer/account?ie=UTF8&action=billing-preferences). This also means making
a bucket to store the output in (those bastards, charging us to host our own billing data!), and setting up an
appropriate policy for that bucket.

1. Wait an hour for your first usage report to be generated. 😴

1. Install django-aws-billing:

    ```bash
    pip install django-aws-billing
    ```

1. Set your AWS credentials in your Django settings:

    ```python
    AWS_ACCESS_KEY = 'AKDERPDERPDERPDERPDERP'
    AWS_SECRET_ACCESS_KEY = 'iL+HERPHERPHERPHERPHERPHERPSQUIRT'
    AWS_BILLING_BUCKET = 'your-aws-billing-info-bucket-name'
    AWS_ACCOUNT_ID = '1234-5679-0000' # Find this number from your AWS Manage Account page: https://portal.aws.amazon.com/gp/aws/manageYourAccount
    ```

1. Add 'aws\_billing' to your INSTALLED\_APPS:

    ```bash
    INSTALLED_APPS = (
        ...
        'aws_billing',
        ...
     )
    ```

1. Run syncdb:

    ```bash
    python manage.py syncdb
    ```

1. Run the billing command:

    ```bash
    python manage.py process_aws_billing
    ```

1. You can then see the costs with:

    ```bash
    python manage.py aws_costs
    ```

## Programmatic Usage

1. Import it and call it!

    ```python
    from aws_billing import aws_billing
    aws_billing.get_cost_for_resource('your-resource-name') # 12.002415
    aws_billing.get_total_cost() # 42.001234
    aws_billing.get_all_costs_by_resource() # {'your-resource-name': 12.002415, 'your-other-resource-name': 29.998819}
    ```

Hooray!

## TODO:

* Hopefully, this package will also include utilities to create nice little javascript charts.
* Something something timezones. And date ranges on the utilities.
* Tests
* Your idea here? The future is unwritten..

Issues welcomed, patches thanked, stars appreciated.
