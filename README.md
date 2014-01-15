![Bezos is a Hustler](http://i.imgur.com/Lw15zkJ.jpg)

django-aws-billing
==================

Django AWS Usage/Billing Package. **Work in Progress**. Some of this is based off of [oddskool's aws-billing](https://github.com/oddskool/aws_billing) server.

* Version: 0.0.0
* Status: In Development
* Don't: Use This Yet

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
