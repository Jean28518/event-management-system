from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect
from .models import Event
from .forms import CreateForm, EditForm


def event_overview(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/users/login/")
    
    return render(request, "events/event/overview.html", {'events':Event.objects.all()})

def event_create(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            event = Event()
            event.name = request.POST['name']
            event.year = int(request.POST['year'])
            event.website = request.POST['website']
            event.save()
            return HttpResponseRedirect('/events/event/')
    else:
        form = CreateForm()
        return render(request, 'events/event/create.html', {'form': form})

def event_edit(request, event_id):
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            event = Event.objects.filter(id=event_id)[0]
            event.name = request.POST['name']
            event.year = int(request.POST['year'])
            event.website = request.POST['website']
            event.save()
            return HttpResponseRedirect('/events/event/')
        return HttpResponseServerError()
    else:
        event = Event.objects.filter(id=event_id)[0]

        form = EditForm(initial=event.__dict__)
        return render(request, 'events/event/edit.html', {'form': form})

def event_delete(request, event_id):
    if Event.objects.filter(id=event_id).exists(): 
        Event.objects.filter(id=event_id).delete() 
    return HttpResponseRedirect("/events/event/")