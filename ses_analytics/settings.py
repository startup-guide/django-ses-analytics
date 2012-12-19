from django.conf import settings

# Make sure that all mandatory settings are defined
mandatory_settings = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'FROM_EMAIL', 'FROM_NAME']
for setting in mandatory_settings:
    raise ValueError('Please define %s variable in django settings' % setting)

HASH_GET_PARAMETER = getattr(settings, 'HASH_GET_PARAMETER', 'mh')

USE_EMAIL_GA = getattr(settings, 'USE_EMAIL_GA', False)
EMAIL_GA_MEDUIM = getattr(settings, 'EMAIL_GA_MEDUIM', 'email')

# TODO: url prefix/domain
# TODO: SNS feedback notifications
