import base64
from django.http import HttpResponse, HttpResponseForbidden

from django.contrib.auth import authenticate, login



def get_user(request):
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            if auth[0].lower() == "basic":
                decoded = base64.b64decode(auth[1]).decode('utf-8')
                uname, passwd = decoded.split(':')
                user = authenticate(username=uname, password=passwd)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        request.user = user
                        return user
                    else:                    
                        return "forbidden"
                else:                    
                        return "forbidden"
    else:
        return "auth_requested"



def _get_response_request_authentication():
    response = HttpResponse()
    response.status_code = 401
    response['WWW-Authenticate'] = 'Basic realm="%s"' % "event-managment-system"
    return response

def handle_failed_authorization(user):
    if user == "auth_requested":
        return _get_response_request_authentication()
    elif user == "forbidden":
        return HttpResponseForbidden()