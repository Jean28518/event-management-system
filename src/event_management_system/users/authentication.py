import base64
from http.client import HTTPResponse

from django.contrib.auth import authenticate, login



def get_user(request):
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            # NOTE: We are only support basic authentication for now.
            #
            if auth[0].lower() == "basic":
                print(auth[0])
                print(auth[1])
                decoded = str(base64.b64decode(auth[1]))
                decoded = decoded[2:-1]
                print(decoded)
                uname, passwd = decoded.split(':')
                user = authenticate(username=uname, password=passwd)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        request.user = user
                        return user
    return None



def get_response_request_authentication():
    response = HTTPResponse()
    response.status_code = 401
    response['WWW-Authenticate'] = 'Basic realm="%s"' % "event-managment-system"
    return response