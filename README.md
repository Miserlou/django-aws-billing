django-aws-billing
==================

Djagno AWS Usage/Billing Package. **Work in Progress**. Some of this is based off of [oddskool's aws-billing](https://github.com/oddskool/aws_billing) server.

# Set up

1. First you need to set up [Programmatic Billing
Access](http://docs.aws.amazon.com/awsaccountbilling/latest/about/programaccess.html) from your [billing preferences
page](https://portal.aws.amazon.com/gp/aws/developer/account?ie=UTF8&action=billing-preferences). This also means making
a bucket to store the output in (those bastards, charging us to host our own billing data!), and setting up an
appropriate policy for that bucket.

1. Install django-aws-billing:

    pip install django-aws-billing

1. Set your AWS credentials in your Django settings:

   AWS\_ACCESS\_KEY = 'AKDERPDERPDERPDERPDERP'
   AWS\_SECRET\_ACCESS\_KEY = 'iL+HERPHERPHERPHERPHERPHERPSQUIRT'

1. Add 'aws\_billing' to your INSTALLED\_APPS:

    INSTALLED_APPS = (
        ...
        'aws_billing',
        ...
     )

2. Run the billing command:

    python manage.py process_aws_billing
