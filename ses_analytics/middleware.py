from ses_analytics.models import Email
from ses_analytics.settings import HASH_GET_PARAMETER

class FromEmailMiddleware(object):
    def process_request(self, request):
        message_hash = request.GET.get(HASH_GET_PARAMETER, '')
        if message_hash and len(message_hash)==20:
            for email in Email.objects.filter(hash=message_hash, is_read=False):
                email.mark_read()
