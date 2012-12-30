from datetime import datetime
import hashlib
from urllib import urlencode

from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from bs4 import BeautifulSoup

from ses_analytics.models import Email
from ses_analytics import settings

# TODO: ability to attach files
# TODO: check user's subscription settings? (some emails should be sent anyway)
# TODO: not all tags are allowed in emails (e.g. avoid <p/>) - check and warn
# TODO: minify html before sending
def send_email(to_email, subject, template, ctx, campaign='',
        from_email=settings.FROM_EMAIL, from_name=settings.FROM_NAME, reply_to=None):
    # TODO: generate unsubscribe link with hash (page with confirmation); default place for it in base template
    context = {
        'URL_PREFIX': settings.URL_PREFIX,
        'STATIC_URL': settings.STATIC_URL,
    }
    context.update(ctx)
    html = render_to_string(template, context)

    # TODO: convert html to text
    # TODO: replace <a href="url">text</a> with 'text (url)', no GA tracking in it
    text = html

    # Generate a unique hash used to track email opening
    hash = hashlib.md5(to_email+' '+str(datetime.now())).hexdigest()[:20]

    # GET parameters added to all internal urls
    data = {settings.HASH_GET_PARAMETER: hash}

    if settings.USE_EMAIL_GA and campaign:
        data['utm_campaign'] = campaign
        data['utm_medium'] = settings.EMAIL_GA_MEDUIM

    params = urlencode(data)

    # Add tracking GET parameters to all internal urls
    xml = BeautifulSoup(html, 'lxml')
    for a in xml.find_all('a'):
        url = a.get('href', '')
        if url.startswith(settings.URL_PREFIX):
            # If hash is inside url - move it to the end of the newly generated link
            if '#' in url:
                start, end = url.split('#')
                url = start + ('&' if '?' in url else '?') + params + '#' + end
            else:
                url += ('&' if '?' in url else '?') + params

        a['href'] = url

    # TODO: set redirects to track external links (optional - controlled by setting)

    html = str(xml)

    # Include 1x1 image for tracking email opening
    if settings.EMAIL_OPEN_TRACKING:
        html += '<img src="%s%s?%s=%s" width="1" height="1" />' % (
                settings.URL_PREFIX, reverse('img1x1'),
                settings.HASH_GET_PARAMETER, hash)

    from_str = u'%s <%s>' % (from_name, from_email)
    # TODO: check that email has an appropriate format (like no dot at the end)

    headers = {}
    if reply_to:
        headers['Reply-To'] = reply_to

    # Generate email message with html and text
    msg = EmailMultiAlternatives(subject, text, from_str, [to_email], headers=headers)
    msg.attach_alternative(html, "text/html")

    message = msg.message().as_string()

    email = Email(hash=hash, campaign=campaign, raw_msg=message,
            from_email=from_email, to_email=to_email)
    email.save()

    email.send() # TODO: run it in celery (use select_related)

# TODO: process bounce and spam report SNS messages, update Email and unsubscribe user
# TODO: take quota into account
