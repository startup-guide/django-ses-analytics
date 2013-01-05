from django.db import models
from django.utils import timezone

import boto
from boto.ses import SESConnection

from ses_analytics import settings

__all__ = ('EMAIL_STATUSES', 'Email')

# TODO: model to manage subscription + settings for receiving letters

# TODO: add retry status (if quota was exceeded)
EMAIL_STATUSES = (
    ('sending', u'Not sent yet'),
    ('sent', u'Sent'),
    ('rejected', u'Rejected'),
    ('bounce', u'Bounce'),
    ('spam', u'Spam'),
)

# TODO: distinguish click time and open time
# TODO: add multi-column indices
class Email(models.Model):
    from_email = models.EmailField(db_index=True)
    to_email = models.EmailField(db_index=True)
    raw_msg = models.TextField(blank=True)

    hash = models.CharField(max_length=30, db_index=True)
    campaign = models.CharField(max_length=30, db_index=True, blank=True)

    time = models.DateTimeField(auto_now_add=True, db_index=True)
    status = models.CharField(max_length=9, choices=EMAIL_STATUSES, default='sending', db_index=True)
    is_read = models.BooleanField(default=False)
    read_time = models.DateTimeField(db_index=True, blank=True, null=True)
    error = models.TextField(blank=True)

    def update_status(self, status, error=''):
        """ Update status (other than 'sending') """
        self.status = status
        self.error = error
        self.raw_msg = ''
        self.save()

    def mark_read(self):
        self.read_time = timezone.now()
        self.is_read = True
        self.save()

    # TODO: Add signals to sending emails and receiving feedback
    def send(self):
        conn = boto.connect_ses(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

        try:
            response = conn.send_raw_email(
                raw_message=self.raw_msg.decode('utf8'),
                destinations=self.to_email,
                source=self.from_email
            )
        except SESConnection.ResponseError, err:
            error_keys = ['status', 'reason', 'body', 'request_id',
                    'error_code', 'error_message']
            for key in error_keys:
                print key, getattr(err, key, None)
            # TODO: update_status
            # TODO: what if message is rejected? parse error message
            # TODO: catch different errors and process differently (postpone or cancel)
        else:
            self.update_status('sent')

        # TODO: save message id?
        #response['SendRawEmailResponse']['SendRawEmailResult']['MessageId']
        #response['SendRawEmailResponse']['ResponseMetadata']['RequestId']

    def __unicode__(self):
        return "Email to %s" % self.to_email
