import os.path

from django.http import HttpResponse

# TODO: detect if request is coming from mobile device
def img1x1(request):
    """ 1x1 image which is inserted in emails to track email openning """
    data = open(os.path.normpath(os.path.join(os.path.abspath(__file__), '..', 'static', 'img', '1x1.gif'))).read()
    response = HttpResponse(data, mimetype='image/gif')
    response['Cache-Control'] = 'no-cache'
    return response
