from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^img1x1$', 'ses_analytics.views.img1x1', name='img1x1'), # used to trace email opening
    # TODO: unsubscription and SNS feedback notifications
)
