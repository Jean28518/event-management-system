from this import d
from urllib.request import HTTPRedirectHandler
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect, Http404, HttpResponseBadRequest
from .models import Event, Lecture, Room
from .forms import CreateEventForm, CreateRoomForm, EditEventForm, EditRoomForm, LectureForm, LectureSubmitForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def event_overview(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/users/login/")
    
    return render(request, "events/event/overview.html", {'events':Event.objects.all()})

def event_create(request):
    if request.method == 'POST':
        form = CreateEventForm(request.POST)
        if form.is_valid():
            event = Event()
            event.name = request.POST['name']
            event.year = int(request.POST['year'])
            event.website = request.POST['website']
            event.save()
            return HttpResponseRedirect('/events/event/')
    else:
        form = CreateEventForm()
        return render(request, 'events/event/create.html', {'form': form})

def event_edit(request, event_id):
    if request.method == 'POST':
        form = EditEventForm(request.POST)
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

        form = EditEventForm(initial=event.__dict__)
        return render(request, 'events/event/edit.html', {'form': form, 'event': event})

def event_delete(request, event_id):
    if Event.objects.filter(id=event_id).exists(): 
        Event.objects.filter(id=event_id).delete() 
    return HttpResponseRedirect("/events/event/")

def event_timeslot_add(request, event_id):
    if Event.objects.filter(id=event_id).exists(): 
        if request.method == 'POST':
            event = Event.objects.filter(id=event_id)[0]
            new_timeslot = request.POST['new_timeslot']
            event.available_timeslots += f"{new_timeslot};"
            event.save()
            return HttpResponseRedirect(f"/events/event/{event_id}/timeslot/")
        else:
            return HttpResponseBadRequest()
    return Http404()

def event_timeslot_remove(request, event_id, index):
    if Event.objects.filter(id=event_id).exists(): 
        event = Event.objects.filter(id=event_id)[0]
        timeslot_strings = event.available_timeslots.split(";")
        del timeslot_strings[index]
        timeslot_return_value = ""
        for timeslot_string in timeslot_strings:
            if timeslot_string != "":
                timeslot_return_value += f"{timeslot_string};"
        event.available_timeslots = timeslot_return_value
        event.save()
    return HttpResponseRedirect(f"/events/event/{event_id}/timeslot/")

def event_timeslot(reqeust, event_id):
    if Event.objects.filter(id=event_id).exists(): 
        event = Event.objects.filter(id=event_id)[0]
        timeslots = _get_timeslots_of_string(event.available_timeslots)
        return render(reqeust, 'events/event/timeslot.html', {'event_name': event.name, 'event_id': event.id, 'timeslots': timeslots})

class Timeslot: 
    text = ""
    id = -1
    checked = False

def _get_timeslots_of_string(string):
    timeslot_strings = string.split(";")
    del timeslot_strings[-1]
    timeslots = []
    for i in range(len(timeslot_strings)):
        timeslot = Timeslot()
        timeslot.text = timeslot_strings[i]
        timeslot.id = i
        timeslots.append(timeslot)
    return timeslots

def _get_string_of_timeslots(timeslots):
    string = ""
    for timeslot in timeslots:
        string += f"{timeslot.text};"
    return string


# Rooms

def room_overview(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/users/login/")
    
    return render(request, "events/room/overview.html", {'rooms':Room.objects.all()})

def room_create(request):
    if request.method == 'POST':
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            room = Room()
            room.name = request.POST['name']
            room.website = request.POST['website']
            room.coordinates = request.POST['coordinates']
            room.save()
            return HttpResponseRedirect('/events/room/')
    else:
        form = CreateRoomForm()
        return render(request, 'events/room/create.html', {'form': form})

def room_edit(request, room_id):
    if request.method == 'POST':
        form = EditRoomForm(request.POST)
        if form.is_valid():
            room = Room.objects.filter(id=room_id)[0]
            room.name = request.POST['name']
            room.website = request.POST['website']
            room.coordinates = request.POST['coordinates']
            room.save()
            return HttpResponseRedirect('/events/room/')
        return HttpResponseServerError()
    else:
        room = Room.objects.filter(id=room_id)[0]

        form = EditRoomForm(initial=room.__dict__)
        return render(request, 'events/room/edit.html', {'form': form, 'room': room})

def room_delete(request, room_id):
    if Room.objects.filter(id=room_id).exists(): 
        Room.objects.filter(id=room_id).delete() 
    return HttpResponseRedirect("/events/room/")


# Lectures:
def lecture_public_create_entry(request, event_id):
    if request.method == 'POST':
        user = authenticate(username=request.POST['email'], password=request.POST['password'])
        if user.is_authenticated:
            login(request, user)
            return HttpResponseRedirect(f"/events/{event_id}/lecture/public/create/?email={user.username}")
        else:
            form = LoginForm()
            return render(request, 'events/lecture/public/create_entry.html', {'form': form, 'login_failed': True})
    else:
        if request.user is not None:
            form = LoginForm()
            return render(request, 'events/lecture/public/create_entry.html', {'form': form, 'login_failed': False})

def lecture_public_create(request, event_id):
    if request.method == 'POST':
        event = Event.objects.filter(id=event_id)[0]
        form = LectureSubmitForm(request.POST)
        if form.is_valid():
            lecture = Lecture()
            lecture.presentator = User.objects.filter(email=request.GET['email'])[0]
            lecture.event = event
            lecture.title = request.POST['title']
            lecture.description = request.POST['description']
            lecture.target_group = request.POST['target_group']
            lecture.qualification_for_lecture = request.POST['qualification_for_lecture']
            lecture.preferred_presentation_style = request.POST['preferred_presentation_style']
            lecture.questions_during_lecture = (request.POST.get('questions_during_lecture', "off") == "on")
            lecture.questions_after_lecture = (request.POST.get('questions_after_lecture', "off") == "on")
            lecture.minimal_lecture_length = int(request.POST['minimal_lecture_length'])
            lecture.maximal_lecture_length = int(request.POST['maximal_lecture_length'])
            lecture.additional_information_by_presentator = request.POST['additional_information_by_presentator']
            lecture.related_website = request.POST['related_website']

            event_timeslots = _get_timeslots_of_string(event.available_timeslots)
            available_timeslots = []
            for event_timeslot in event_timeslots:
                if (request.POST.get(f"timeslot_{event_timeslot.id}", "off") == ""):
                    available_timeslots.append(event_timeslot)
            lecture.available_timeslots = _get_string_of_timeslots(available_timeslots)
            lecture.save()
            return HttpResponseRedirect('/events/room/')
    else:
        form = LectureSubmitForm()
        event = Event.objects.filter(id=event_id)[0]
        return render(request, 'events/lecture/public/create.html', {'form': form, 'event': event, 'timeslots': _get_timeslots_of_string(event.available_timeslots)})

def lecture_overview(request, event_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/users/login/")
    event = Event.objects.filter(id=event_id)[0]
    lectures = Lecture.objects.filter(event=event).all()
    
    return render(request, "events/lecture/overview.html", {'lectures': lectures, 'event': event})

def lecture_create(request, event_id):
    if request.method == 'POST':
        form = LectureForm(request.POST)
        if form.is_valid():
            lecture = Lecture()
            _saveLectureFromFullEdit(request, lecture)
            return HttpResponseRedirect(f'/events/{lecture.event.id}/lecture/overview/')
    else:
        form = LectureForm({'event': event_id})
        return render(request, 'events/lecture/create.html', {'form': form, 'timeslots': _get_timeslots_of_string(Event.objects.get(id=event_id).available_timeslots), 'event_id': event_id})

def lecture_edit(request, lecture_id):
    lecture = Lecture.objects.filter(id=lecture_id).select_related('event').select_related('presentator').select_related('attendant').select_related('scheduled_in_room')[0]
    if request.method == 'POST':
        form = LectureForm(request.POST)
        if form.is_valid():
            _saveLectureFromFullEdit(request, lecture)
            return HttpResponseRedirect(f'/events/{lecture.event.id}/lecture/overview/')
    else:
        data = lecture.__dict__
        data['event'] = lecture.event.id
        data['presentator'] = lecture.presentator.id
        if lecture.attendant:
            data['attendant'] = lecture.attendant.id
        if lecture.scheduled_in_room:
            data['scheduled_in_room'] = lecture.scheduled_in_room.id
        form = LectureForm(data=data)
        print(lecture.available_timeslots)
        all_timeslots = _get_timeslots_of_string(lecture.event.available_timeslots)
        available_timeslots = _get_timeslots_of_string(lecture.available_timeslots)
        for timeslot in available_timeslots: 
            for all_timeslot in all_timeslots:
                if all_timeslot.text == timeslot.text:     
                    all_timeslot.checked = True
        return render(request, 'events/lecture/edit.html', {'form': form, 'lecture': lecture, 'timeslots': all_timeslots})


def _saveLectureFromFullEdit(request, lecture):
    print(request.POST)
    if request.POST['presentator'] != "":
        lecture.presentator = User.objects.filter(id=request.POST['presentator'])[0]
    if request.POST['event'] != "":
        lecture.event = Event.objects.filter(id=request.POST['event'])[0]
    if request.POST['attendant'] != "":
        lecture.attendant = User.objects.filter(id=request.POST['attendant'])[0]
    else:
        lecture.attendant = None
    if request.POST['scheduled_in_room'] != "":
        lecture.scheduled_in_room = Room.objects.filter(id=request.POST['scheduled_in_room'])[0]
    else:
        lecture.scheduled_in_room = None
    lecture.title = request.POST['title']
    lecture.description = request.POST['description']
    lecture.target_group = request.POST['target_group']
    lecture.qualification_for_lecture = request.POST['qualification_for_lecture']
    lecture.preferred_presentation_style = request.POST['preferred_presentation_style']
    lecture.questions_during_lecture = (request.POST.get('questions_during_lecture', "off") == "on")
    lecture.questions_after_lecture = (request.POST.get('questions_after_lecture', "off") == "on")
    lecture.minimal_lecture_length = int(request.POST['minimal_lecture_length'])
    lecture.maximal_lecture_length = int(request.POST['maximal_lecture_length'])
    lecture.additional_information_by_presentator = request.POST['additional_information_by_presentator']
    lecture.related_website = request.POST['related_website']
    if request.POST['scheduled_presentation_time'] != "":
        lecture.scheduled_presentation_time = request.POST['scheduled_presentation_time']
    lecture.scheduled_presentation_length = int(request.POST['scheduled_presentation_length'])
    lecture.scheduled_presentation_style = request.POST['scheduled_presentation_style']
    lecture.further_information = request.POST['further_information']
    lecture.link_to_material = request.POST['link_to_material']
    lecture.link_to_recording = request.POST['link_to_recording']
    

    event_timeslots = _get_timeslots_of_string(lecture.event.available_timeslots)
    available_timeslots = []
    for event_timeslot in event_timeslots:
        if (request.POST.get(f"timeslot_{event_timeslot.id}", "off") == ""):
            available_timeslots.append(event_timeslot)
    lecture.available_timeslots = _get_string_of_timeslots(available_timeslots)
    lecture.save()

def lecture_delete(request, lecture_id):
    event_id = 0
    if Lecture.objects.filter(id=lecture_id).exists(): 
        lecture = Lecture.objects.get(id=lecture_id)
        event_id = lecture.event.id
        lecture.delete()
    return HttpResponseRedirect(f"/events/{event_id}/lecture/overview/")

def enable_call_for_papers(request, event_id):
    event = Event.objects.get(id=event_id)
    event.call_for_papers = True
    event.save()
    return HttpResponseRedirect(f"/events/{event_id}/lecture/overview/")

def disable_call_for_papers(request, event_id):
    event = Event.objects.get(id=event_id)
    event.call_for_papers = False
    event.save()
    return HttpResponseRedirect(f"/events/{event_id}/lecture/overview/")
    