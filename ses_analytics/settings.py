from django.conf import settings

# Make sure that all mandatory settings are defined
mandatory_settings = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'FROM_EMAIL',
        'FROM_NAME', 'URL_PREFIX', 'STATIC_URL']
for setting in mandatory_settings:
    if not hasattr(settings, setting):
        raise ValueError('Please define %s variable in django settings' % setting)
    else:
        globals()[setting] = getattr(settings, setting)

HASH_GET_PARAMETER = getattr(settings, 'HASH_GET_PARAMETER', 'mh')

USE_EMAIL_GA = getattr(settings, 'USE_EMAIL_GA', False) # TODO: rename to INTERNAL_CLICK_TRACKING?
EMAIL_GA_MEDUIM = getattr(settings, 'EMAIL_GA_MEDUIM', 'email')

EMAIL_OPEN_TRACKING = getattr(settings, 'EMAIL_OPEN_TRACKING', True)

# TODO: url prefix/domain
# TODO: SNS feedback notifications
# TODO: external click tracking
