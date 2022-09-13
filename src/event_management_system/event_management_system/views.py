from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from . import set_rights


def index(request):
    set_rights.init()
    if User.objects.count() == 0:
        return HttpResponseRedirect("/users/register/?next=/")
    return HttpResponseRedirect("/users/")