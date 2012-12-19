import os.path

from django.http import HttpResponse

def img1x1(request):
    """ 1x1 image which is inserted in emails to track email openning """
    data = open(os.path.join(os.path.join(os.path.abspath(__file__), '..'), 'static', 'img', '1x1.gif')).read()
    response = HttpResponse(data, mimetype='image/gif')
    response['Cache-Control'] = 'no-cache'
    return response
