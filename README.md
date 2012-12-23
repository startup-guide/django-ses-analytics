django-ses-analytics
====================

Send emails and collect analytics in Django with Amazon SES.

Features
========

* Sending emails using Amazon SES
* Track opening emails
* Track clicking on internal and external links
* Google analytics integrated
* Detailed statistics on emails sent
* Process bounces and complaints

Configuration
=============

Specify the following parameters:
* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
* FROM_EMAIL - email from which emails are sent
* FROM_NAME - the name of the sender
* URL_PREFIX - url prefix (say, 'http://127.0.0.1:8000')
* HASH_GET_PARAMETER (optional, 'mh' by default) - get parameter added to internal links inside emails to track clicks
* USE_EMAIL_GA (optional, False by default)
* EMAIL_GA_MEDUIM (optional, 'email' by default)

Add 'ses_analytics.middleware.FromEmailMiddleware' to MIDDLEWARE_CLASSES (position doesn't matter).

Add 'ses_analytics' to INSTALLED_APPS.

Add url(r'^', include('ses_analytics.urls')) to urlpatterns.

Amazon SES configuration
========================

Go to Amazon SES console https://console.aws.amazon.com/ses/home , add verified sender email,
verify the email and enable DKIM signing.

TODO
====

* Unsubscribe
* Process bounces and spam complaints (see http://bouncely.com/), use SNS
* Automatically generate a text version of email from HTML version
* Suggest metrics to investigate
* Track opening external links
* Provide a nice name for displaying in admin

