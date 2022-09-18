from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import redirect

from . import set_rights


def index(request):
    set_rights.init()
    if User.objects.count() == 0:
        return HttpResponseRedirect("/users/register/?next=/")
    if request.user.groups.filter(name='Contact').exists():
        return redirect('lecture_contact_overview')
    return redirect('event_overview')