from datetime import datetime
import hashlib
from urllib import urlencode

from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from lxml.etree import tostring
from lxml.html.soupparser import fromstring

from ses_analytics.models import Email
from ses_analytics import settings

# TODO: ability to attach files
# TODO: check user's subscription settings? (some emails should be sent anyway)
# TODO: not all tags are allowed in emails (e.g. avoid <p/>) - check and warn
def send_email(recipient, subject, template, ctx, campaign='', from_email=settings.FROM_EMAIL,
        from_name=settings.FROM_NAME, reply_to=None, to_email=None):
    """ To send emails to admin account set recipient=None """
    # TODO: generate unsubscribe link with hash (page with confirmation); default place for it in base template
    context = {}
    context.update(ctx)
    context['recipient'] = recipient
    html = render_to_string(template, context)

    # TODO: convert html to text
    # TODO: replace <a href="url">text</a> with 'text (url)', no GA tracking in it
    text = html

    # Generate a unique hash used to track email opening
    name = str(recipient.user_id) if recipient else '' # TODO: fix it
    hash = hashlib.md5(name+' '+str(datetime.now())).hexdigest()[:20]

    # GET parameters added to all internal urls
    data = {settings.HASH_GET_PARAMETER: hash}

    if settings.USE_GA_CAMPAIGN and campaign:
        data['utm_campaign'] = campaign
        data['utm_medium'] = settings.EMAIL_GA_MEDUIM

    params = urlencode(data)

    # Add tracking GET parameters to all internal urls
    xml = fromstring(html)
    for a in xml.findall('.//a'):
        url = a.get('href')
        if url.startswith(settings.URL_PREFIX):
            # If hash is inside url - move it to the end of the newly generated link
            if '#' in url:
                start, end = url.split('#')
                url = start + ('&' if '?' in url else '?') + params + '#' + end
            else:
                url += ('&' if '?' in url else '?') + params

        a.set('href', url)

    # TODO: set redirects to track external links (optional - controlled by setting)

    html = tostring(xml)

    # Include 1x1 image for tracking email opening
    # TODO: fix URL_PREFIX
    img_url = '{{ URL_PREFIX }}%s?%s=%s' % (reverse('img1x1'), settings.HASH_GET_PARAMETER, hash))
    html += '<img src="%s" width="1" height="1" />' % img_url

    from_str = u'%s <%s>' % (from_email, from_name)
    if to_email is None:
        to_email = recipient.user.email if recipient else settings.ADMIN_EMAIL
    # TODO: check that email has appropriate format (like no dot at the end)

    headers = {}
    if reply_to:
        headers['Reply-To'] = reply_to

    # Generate email message with html and text
    msg = EmailMultiAlternatives(subject, text, from_str, [to_email], headers=headers)
    msg.attach_alternative(html, "text/html")

    message = msg.message().as_string()

    email = Email(recipient=recipient, hash=hash, campaign=campaign, raw_msg=message,
            from_email=from_email, to_email=to_email)
    email.save()

    email.send() # TODO: run it in celery (use select_related)

# TODO: task which retrives bounce and spam report mails, extracts data, updates Email and unsubscribes user
# TODO: take quota into account
