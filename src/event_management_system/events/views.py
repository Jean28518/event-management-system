from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect, Http404, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound
from .models import Event, Lecture, Room
from .forms import RoomFrom, EventForm, LectureForm, LectureSubmitForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect
import csv
from event_management_system.meta import meta
from django.template.defaultfilters import date as _date
from .custom_question import string2custom_questions, custom_question, add_custom_question_to_array, custom_questions2string, remove_custom_question_from_array, post_answer2custom_answers_string, string2question_answer_pairs
from .field_activation import post_answer2string_disabled_entries, string_disabled_entries2field_activation_entries
from django.views.decorators.clickjacking import xframe_options_exempt
from datetime import timedelta
from django.utils import timezone
from django.views.decorators.cache import cache_page


@permission_required("events.view_event")
def event_overview(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/users/login/")
    
    return render(request, "events/event/overview.html", {'request_user': request.user, 'events':Event.objects.all()})

@permission_required("events.add_event")
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = Event()
            event.name = request.POST['name']
            event.year = int(request.POST['year'])
            event.website = request.POST['website']
            event.live_board_default = request.POST['live_board_default']
            event.save()
            return HttpResponseRedirect('/events/event/')
    else:
        form = EventForm()
        return render(request, 'events/event/create.html', {'request_user': request.user, 'form': form})

@permission_required("events.change_event")
def event_edit(request, event_id):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = Event.objects.filter(id=event_id)[0]
            event.name = request.POST['name']
            event.year = int(request.POST['year'])
            event.website = request.POST['website']
            event.live_board_default = request.POST['live_board_default']
            event.save()
            return HttpResponseRedirect('/events/event/')
        return HttpResponseServerError()
    else:
        event = Event.objects.filter(id=event_id)[0]


        form = EventForm(initial=event.__dict__)
        return render(request, 'events/event/edit.html', {'request_user': request.user, 'form': form, 'event': event})

@permission_required("events.delete_event")
def event_delete(request, event_id):
    if Event.objects.filter(id=event_id).exists(): 
        Event.objects.filter(id=event_id).delete() 
    return HttpResponseRedirect("/events/event/")

@permission_required("events.change_event")
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

@permission_required("events.change_event")
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

@permission_required("events.change_event")
def event_timeslot(request, event_id):
    if Event.objects.filter(id=event_id).exists(): 
        event = Event.objects.filter(id=event_id)[0]
        timeslots = _get_timeslots_of_string(event.available_timeslots)
        return render(request, 'events/event/timeslot.html', {'request_user': request.user, 'event_name': event.name, 'event_id': event.id, 'timeslots': timeslots})

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
@permission_required("events.view_room")
def room_overview(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/users/login/")
    
    return render(request, "events/room/overview.html", {'request_user': request.user, 'rooms':Room.objects.all()})

@permission_required("events.add_room")
def room_create(request):
    if request.method == 'POST':
        form = RoomFrom(request.POST)
        if form.is_valid():
            room = Room()
            room.name = request.POST['name']
            room.website = request.POST['website']
            room.coordinates = request.POST['coordinates']
            room.save()
            return HttpResponseRedirect('/events/room/')
    else:
        form = RoomFrom()
        return render(request, 'events/room/create.html', {'request_user': request.user, 'form': form})

@permission_required("events.change_room")
def room_edit(request, room_id):
    if request.method == 'POST':
        form = RoomFrom(request.POST)
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

        form = RoomFrom(initial=room.__dict__)
        return render(request, 'events/room/edit.html', {'request_user': request.user, 'form': form, 'room': room})

@permission_required("events.delete_room")
def room_delete(request, room_id):
    if Room.objects.filter(id=room_id).exists(): 
        Room.objects.filter(id=room_id).delete() 
    return HttpResponseRedirect("/events/room/")


# Lectures:
# @permission_required("events.add_lecture")
def lecture_public_create_entry(request, event_id):
    if request.user.is_authenticated:
        return HttpResponseRedirect(f"/events/{event_id}/lecture/public/create/?email={request.user.username}")
    if request.method == 'POST':
        user = authenticate(username=request.POST['email'], password=request.POST['password'])
        if user.is_authenticated:
            login(request, user)
            return HttpResponseRedirect(f"/events/{event_id}/lecture/public/create/?email={user.username}")
        else:
            form = LoginForm()
            return render(request, 'events/lecture/public/create_entry.html', {'request_user': request.user, 'form': form, 'login_failed': True, 'event_id': event_id})
    else:
        if request.user is not None:
            form = LoginForm()
            return render(request, 'events/lecture/public/create_entry.html', {'request_user': request.user, 'form': form, 'login_failed': False, 'event_id': event_id})

@permission_required("events.add_lecture")
def lecture_public_create(request, event_id):
    event = Event.objects.filter(id=event_id)[0]
    if request.method == 'POST':
        form = LectureSubmitForm(request.POST)
        lecture = Lecture()
        lecture.presentator = request.user
        lecture.event = event
        _save_lecture_from_presentator_edit(request, lecture)
        return redirect('lecture_public_created_successfully', event_id)
    # if request.method == 'POST':
    #     event = Event.objects.filter(id=event_id)[0]
    #     form = LectureSubmitForm(request.POST)
    #     if form.is_valid():
    #         lecture = Lecture()
    #         lecture.presentator = request.user
    #         lecture.event = event
    #         lecture.title = request.POST['title']
    #         lecture.description = request.POST['description']
    #         lecture.target_group = request.POST['target_group']
    #         lecture.qualification_for_lecture = request.POST['qualification_for_lecture']
    #         lecture.preferred_presentation_style = request.POST['preferred_presentation_style']
    #         lecture.questions_during_lecture = (request.POST.get('questions_during_lecture', "off") == "on")
    #         lecture.questions_after_lecture = (request.POST.get('questions_after_lecture', "off") == "on")
    #         lecture.minimal_lecture_length = int(request.POST['minimal_lecture_length'])
    #         lecture.maximal_lecture_length = int(request.POST['maximal_lecture_length'])
    #         lecture.additional_information_by_presentator = request.POST['additional_information_by_presentator']
    #         lecture.related_website = request.POST['related_website']

    #         event_timeslots = _get_timeslots_of_string(event.available_timeslots)
    #         available_timeslots = []
    #         for event_timeslot in event_timeslots:
    #             if (request.POST.get(f"timeslot_{event_timeslot.id}", "off") == ""):
    #                 available_timeslots.append(event_timeslot)
    #         lecture.available_timeslots = _get_string_of_timeslots(available_timeslots)
    #         lecture.save()
    #         return HttpResponseRedirect(f'/events/{event_id}/lecture/public/created_success')
    else:
        form = LectureSubmitForm()
        event = Event.objects.filter(id=event_id)[0]
        custom_question_answer_pairs = string2question_answer_pairs("", event.custom_questions)
        return render(request, 'events/lecture/public/create.html',
                {'request_user': request.user, 'form': form, 'event': event, 'timeslots': _get_timeslots_of_string(event.available_timeslots),
                'custom_question_answer_pairs': custom_question_answer_pairs})

def lecture_public_created_successfully(request, event_id):
    return render(request, 'events/lecture/public/create_successful.html', {'event_id': event_id})


@permission_required("events.view_lecture")
def lecture_overview(request, event_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/users/login/")
    event = Event.objects.filter(id=event_id)[0]
    lectures = Lecture.objects.filter(event=event).all()
    lectures_empty = Lecture.objects.filter(event=event).count() == 0
    no_timeslots_defined = False
    if len(_get_timeslots_of_string(event.available_timeslots)) == 0:
        no_timeslots_defined = True
    return render(request, "events/lecture/overview.html", {
        'request_user': request.user, 
        'lectures': lectures, 
        'event': event, 
        'lectures_empty': lectures_empty, 
        'no_timeslots_defined': no_timeslots_defined})


@permission_required("events.add_lecture")
def lecture_create(request, event_id):
    if request.method == 'POST':
        form = LectureForm(request.POST)
        if form.is_valid():
            lecture = Lecture()
            _save_lecture_from_full_edit(request, lecture)
            return HttpResponseRedirect(f'/events/{lecture.event.id}/lecture/overview/')
    else:
        form = LectureForm({'event': event_id})
        event = Event.objects.filter(id=event_id)[0]
        custom_question_answer_pairs = string2question_answer_pairs("", event.custom_questions)
        form = _remove_disabled_fields(form, event)
        return render(request, 'events/lecture/create.html', 
                {'form': form, 
                'timeslots': _get_timeslots_of_string(Event.objects.get(id=event_id).available_timeslots), 
                'event_id': event_id,
                'custom_question_answer_pairs': custom_question_answer_pairs})


@permission_required("events.change_lecture")
def lecture_edit(request, lecture_id):
    lecture = Lecture.objects.filter(id=lecture_id).select_related('event').select_related('presentator').select_related('attendant').select_related('scheduled_in_room')[0]
    if request.method == 'POST':
        form = LectureForm(request.POST)
        _save_lecture_from_full_edit(request, lecture)
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
        all_timeslots = _get_timeslots_of_string(lecture.event.available_timeslots)
        available_timeslots = _get_timeslots_of_string(lecture.available_timeslots)
        for timeslot in available_timeslots: 
            for all_timeslot in all_timeslots:
                if all_timeslot.text == timeslot.text:     
                    all_timeslot.checked = True
        custom_question_answer_pairs = string2question_answer_pairs(lecture.custom_question_answers, lecture.event.custom_questions)

        form = _remove_disabled_fields(form, lecture.event)

        return render(request, 'events/lecture/edit.html',
                      {'request_user': request.user, 'form': form, 'lecture': lecture, 'timeslots': all_timeslots, "custom_question_answer_pairs": custom_question_answer_pairs})


def _remove_disabled_fields(form, event):
    for disabled_field in event.disabled_fields.split(";"):
        if disabled_field == "":
            continue
        if disabled_field.endswith("_id"):
            disabled_field = disabled_field.replace("_id", "")
        if disabled_field in form.fields.keys():
            del form.fields[disabled_field]
    return form

@permission_required("events.view_lecture")
def lecture_view(request, lecture_id):
    lecture = Lecture.objects.filter(id=lecture_id).select_related('event').select_related('presentator').select_related('attendant').select_related('scheduled_in_room')[0]
    data = lecture.__dict__
    data['event'] = lecture.event.id
    data['presentator'] = lecture.presentator.id
    if lecture.attendant:
        data['attendant'] = lecture.attendant.id
    if lecture.scheduled_in_room:
        data['scheduled_in_room'] = lecture.scheduled_in_room.id
    form = LectureForm(initial=data)
    all_timeslots = _get_timeslots_of_string(lecture.event.available_timeslots)
    available_timeslots = _get_timeslots_of_string(lecture.available_timeslots)
    for timeslot in available_timeslots: 
        for all_timeslot in all_timeslots:
            if all_timeslot.text == timeslot.text:     
                all_timeslot.checked = True
    custom_question_answer_pairs = string2question_answer_pairs(lecture.custom_question_answers, lecture.event.custom_questions)
    # Disable Form Field because of view
    for field in form.fields:
        form.fields[field].disabled = True

    form = _remove_disabled_fields(form, lecture.event)

    return render(request, 'events/lecture/view.html',
                    {'request_user': request.user, 'form': form, 'lecture': lecture, 'timeslots': all_timeslots,
                    'custom_question_answer_pairs': custom_question_answer_pairs, "disabled": True})

def lecture_contact_overview(request):
    lectures = Lecture.objects.filter(presentator=request.user.id)
    return render(request, 'events/lecture/contact/overview.html', {'request_user': request.user, 'lectures': lectures})

def lecture_contact_create_entry(request):
    events = Event.objects.all()
    return render(request, 'events/lecture/contact/select_event_for_submit.html', {'request_user': request.user, 'events': events})


def lecture_contact_edit(request, lecture_id):
    if not Lecture.objects.filter(id=lecture_id).exists():
        return HttpResponseNotFound()
    lecture = Lecture.objects.get(id=lecture_id)
    user = request.user
    if not _does_contact_user_has_access_to_lecture(user, lecture):
        return HttpResponseNotAllowed()
    if request.method == 'POST':
        form = LectureSubmitForm(request.POST)
        _save_lecture_from_presentator_edit(request, lecture)
        return redirect('lecture_contact_overview')
    else:
        data = lecture.__dict__
        form = LectureSubmitForm(data=data)
        all_timeslots = _get_timeslots_of_string(lecture.event.available_timeslots)
        available_timeslots = _get_timeslots_of_string(lecture.available_timeslots)
        for timeslot in available_timeslots: 
            for all_timeslot in all_timeslots:
                if all_timeslot.text == timeslot.text:     
                    all_timeslot.checked = True
        custom_question_answer_pairs = string2question_answer_pairs(lecture.custom_question_answers, lecture.event.custom_questions)
        form = _remove_disabled_fields(form, lecture.event)
        return render(request, 'events/lecture/contact/edit.html',
                      {'request_user': request.user, 'form': form, 'lecture': lecture, 'timeslots': all_timeslots,
                    'custom_question_answer_pairs': custom_question_answer_pairs})

# If This is a contact user, which has access
def _does_contact_user_has_access_to_lecture(user, lecture):
    if not user.groups.filter(name='Contact').exists() or lecture.presentator != user:
        return False
    return True


def lecture_contact_view(request, lecture_id):
    if not Lecture.objects.filter(id=lecture_id).exists():
        return HttpResponseNotFound()
    lecture = Lecture.objects.get(id=lecture_id)
    user = request.user
    if not _does_contact_user_has_access_to_lecture(user, lecture):
        return HttpResponseNotAllowed()
    lecture = Lecture.objects.filter(id=lecture_id)[0]
    data = lecture.__dict__
    data['event'] = lecture.event.id
    data['presentator'] = lecture.presentator.id
    if lecture.attendant:
        data['attendant'] = lecture.attendant.id
    if lecture.scheduled_in_room:
        data['scheduled_in_room'] = lecture.scheduled_in_room.id
    form = LectureSubmitForm(initial=data)
    print(lecture.available_timeslots)
    all_timeslots = _get_timeslots_of_string(lecture.event.available_timeslots)
    available_timeslots = _get_timeslots_of_string(lecture.available_timeslots)
    for timeslot in available_timeslots: 
        for all_timeslot in all_timeslots:
            if all_timeslot.text == timeslot.text:     
                all_timeslot.checked = True
    custom_question_answer_pairs = string2question_answer_pairs(lecture.custom_question_answers, lecture.event.custom_questions)
    form = _remove_disabled_fields(form, lecture.event)
    # Disable Form Field because of view
    for field in form.fields:
        form.fields[field].disabled = True
    return render(request, 'events/lecture/contact/view.html',
                    {'request_user': request.user, 'form': form, 'lecture': lecture, 'timeslots': all_timeslots,
                    'custom_question_answer_pairs': custom_question_answer_pairs, "disabled": True})

@permission_required("events.change_lecture")
def _save_lecture_from_full_edit(request, lecture):
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
    # TODO: (duplicate) - globalize
    lecture.title = request.POST.get('title', "")
    lecture.description = request.POST.get('description', "")
    lecture.target_group = request.POST.get('target_group', "")
    lecture.qualification_for_lecture = request.POST.get('qualification_for_lecture', "")
    lecture.preferred_presentation_style = request.POST.get('preferred_presentation_style', "")
    lecture.questions_during_lecture = (request.POST.get('questions_during_lecture', "off") == "on")
    lecture.questions_after_lecture = (request.POST.get('questions_after_lecture', "off") == "on")
    lecture.minimal_lecture_length = int(request.POST.get('minimal_lecture_length', "0"))
    lecture.maximal_lecture_length = int(request.POST.get('maximal_lecture_length', "0"))
    lecture.additional_information_by_presentator = request.POST.get('additional_information_by_presentator', "")
    lecture.related_website = request.POST.get('related_website', "")
    if request.POST.get('scheduled_presentation_time', "") != "":
        lecture.scheduled_presentation_time = request.POST.get('scheduled_presentation_time', "")
    if request.POST.get('scheduled_presentation_length', "") != "":
        lecture.scheduled_presentation_length = int(request.POST.get('scheduled_presentation_length', ""))
    lecture.scheduled_presentation_style = request.POST.get('scheduled_presentation_style', "")
    lecture.further_information = request.POST.get('further_information', "")
    lecture.link_to_material = request.POST.get('link_to_material', "")
    lecture.link_to_recording = request.POST.get('link_to_recording', "")

    event_timeslots = _get_timeslots_of_string(lecture.event.available_timeslots)
    available_timeslots = []
    for event_timeslot in event_timeslots:
        if (request.POST.get(f"timeslot_{event_timeslot.id}", "off") == ""):
            available_timeslots.append(event_timeslot)
    lecture.available_timeslots = _get_string_of_timeslots(available_timeslots)
    lecture.custom_question_answers = post_answer2custom_answers_string(request, lecture.event.custom_questions)
    lecture.save()

def _save_lecture_from_presentator_edit(request, lecture):
    lecture.title = request.POST.get('title', "")
    lecture.description = request.POST.get('description', "")
    lecture.target_group = request.POST.get('target_group', "")
    lecture.qualification_for_lecture = request.POST.get('qualification_for_lecture', "")
    lecture.preferred_presentation_style = request.POST.get('preferred_presentation_style', "")
    lecture.questions_during_lecture = (request.POST.get('questions_during_lecture', "off") == "on")
    lecture.questions_after_lecture = (request.POST.get('questions_after_lecture', "off") == "on")
    lecture.minimal_lecture_length = int(request.POST.get('minimal_lecture_length', "0"))
    lecture.maximal_lecture_length = int(request.POST.get('maximal_lecture_length', "0"))
    lecture.additional_information_by_presentator = request.POST.get('additional_information_by_presentator', "")
    lecture.related_website = request.POST.get('related_website', "")

    event_timeslots = _get_timeslots_of_string(lecture.event.available_timeslots)
    available_timeslots = []
    for event_timeslot in event_timeslots:
        if (request.POST.get(f"timeslot_{event_timeslot.id}", "off") == ""):
            available_timeslots.append(event_timeslot)
    lecture.available_timeslots = _get_string_of_timeslots(available_timeslots)
    lecture.custom_question_answers = post_answer2custom_answers_string(request, lecture.event.custom_questions)
    lecture.save()


def lecture_delete(request, lecture_id):
    if not Lecture.objects.filter(id=lecture_id).exists():
        return HttpResponseNotFound()
    lecture = Lecture.objects.get(id=lecture_id)
    user = request.user
    if not _does_contact_user_has_access_to_lecture(user, lecture) and not user.has_perm("events.delete_lecture"):
        return HttpResponseNotAllowed("")
    event_id = 0
    if Lecture.objects.filter(id=lecture_id).exists(): 
        lecture = Lecture.objects.get(id=lecture_id)
        event_id = lecture.event.id
        lecture.delete()
    if _does_contact_user_has_access_to_lecture(user, lecture):
        return redirect("lecture_contact_overview")
    return HttpResponseRedirect(f"/events/{event_id}/lecture/overview/")


@permission_required("events.change_event")
def enable_call_for_papers(request, event_id):
    event = Event.objects.get(id=event_id)
    event.call_for_papers = True
    event.save()
    return HttpResponseRedirect(f"/events/{event_id}/lecture/overview/")


@permission_required("events.change_event")
def disable_call_for_papers(request, event_id):
    event = Event.objects.get(id=event_id)
    event.call_for_papers = False
    event.save()
    return HttpResponseRedirect(f"/events/{event_id}/lecture/overview/")
    
# TODO: Define a apropriate permission
@permission_required('users.delete_profile') 
def lecture_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=lectures.csv'
    
    csv.QUOTE_ALL
    writer = csv.writer(response, quotechar="\"", quoting=csv.QUOTE_ALL, delimiter=";")
    
    
    fields = meta.get_all_fields()

    fields.remove("$user.password")
    fields.remove("$user.is_superuser")
    fields.remove("$user.profile.id")
    fields.remove("$user.profile.user_id")

    fields.remove("$attendant.password")
    fields.remove("$attendant.is_superuser")
    fields.remove("$attendant.profile.id")
    fields.remove("$attendant.profile.user_id")

    writer.writerow(fields)

    lectures = Lecture.objects.all()

    for lecture in lectures:
        user = lecture.presentator
        attendant = lecture.attendant
        room = lecture.scheduled_in_room
        event = lecture.event
        lecture_line = []
        for field in fields:
            if field.startswith("$user."):
                if field.startswith("$user.profile."):
                    lecture_line.append(str(user.profile.__dict__[field.replace("$user.profile.", "")]))
                else:
                    lecture_line.append(str(user.__dict__[field.replace("$user.", "")]))
            if field.startswith("$lecture."):
                lecture_line.append(str(lecture.__dict__[field.replace("$lecture.", "")]))
            if field.startswith("$attendant."):
                if field.startswith("$attendant.profile."):
                    lecture_line.append(str(user.profile.__dict__[field.replace("$attendant.profile.", "")]))
                else:
                    lecture_line.append(str(user.__dict__[field.replace("$attendant.", "")]))
            if field.startswith("$room.") and room:
                lecture_line.append(str(room.__dict__[field.replace("$room.", "")]))
            if field.startswith("$event."):
                lecture_line.append(str(event.__dict__[field.replace("$event.", "")]))
            
        writer.writerow(lecture_line)

    return response

@cache_page(15) # Hold view in cache for 15 seconds
@xframe_options_exempt
def timetable(request, event_id):
    event = Event.objects.filter(id=event_id)
    if not event.exists():
        return HttpResponseBadRequest()
    event = event[0]
    lectures = Lecture.objects.filter(event_id=event.id)

    # Generate days
    days = []
    for lecture in lectures:
        # (lecture.__dict__[keyword.replace("$lecture.", "")], "l, j. F o, H:i")
        day = { "title": _date(lecture.scheduled_presentation_time, "l, j. F o"), "date":str(lecture.scheduled_presentation_time).split(" ")[0] }
        # day = { "date": _date(str(lecture.scheduled_presentation_time).split(" ")[0], "l, j. F o")}
        if not day in days:
            days.append(day)
    days.sort(key=lambda d: str(d["date"]))

    # Generate rooms
    for day in days:
        day["rooms"] = []
        for lecture in lectures:
            if str(lecture.scheduled_presentation_time).split(" ")[0] == day["date"] and lecture.scheduled_in_room:
                
 
                
                # Add lecture to room:
                found_room = {}
                for room in day["rooms"]:
                    if room["name"] == lecture.scheduled_in_room.name:
                        found_room = room
                        break
                if found_room == {}:
                    found_room = {"name": lecture.scheduled_in_room.name, "lectures": [], "website": lecture.scheduled_in_room.website, "id": lecture.scheduled_in_room.id}
                    day["rooms"].append(found_room)
                    day["rooms"].sort(key=lambda d: str(d["id"]))
                lecture.nice_time = _date(lecture.scheduled_presentation_time, "H:i")
                found_room["lectures"].append(lecture)
                found_room["lectures"].sort(key=lambda d: str(d.scheduled_presentation_time))
    return render(request, 'events/lecture/public/timetable.html',
                      {'request_user': request.user, 'event': event, 'days': days})

def event_custom_questions(request, event_id):
    event = Event.objects.filter(id=event_id)
    if not event.exists():
        return HttpResponseBadRequest()
    event = event[0]
    qustom_questions = string2custom_questions(event.custom_questions)
    return render(request, "events/event/custom_fields.html", 
            {'request_user': request.user, 'event': event, 'custom_questions': qustom_questions})

def event_custom_questions_add(request, event_id):
    event = Event.objects.filter(id=event_id)
    if not event.exists():
        return HttpResponseBadRequest()
    event = event[0]
    if request.method == "POST":
        custom_questions = string2custom_questions(event.custom_questions)
        add_custom_question_to_array(custom_questions, request.POST["type"], request.POST["text"])
        event.custom_questions = custom_questions2string(custom_questions)
        event.save()
        return redirect("event_custom_questions", event_id)
    else:
        return HttpResponseBadRequest()

def event_custom_questions_remove(request, event_id, id):
    event = Event.objects.filter(id=event_id)
    if not event.exists():
        return HttpResponseBadRequest()
    event = event[0]
    custom_questions = string2custom_questions(event.custom_questions)
    custom_questions = remove_custom_question_from_array(custom_questions, id)
    event.custom_questions = custom_questions2string(custom_questions)
    event.save()
    return redirect("event_custom_questions", event_id)
        

def event_field_activation(request, event_id):
    event = Event.objects.filter(id=event_id)
    if not event.exists():
        return HttpResponseBadRequest()
    event = event[0]
    if request.method == "POST":
        event.disabled_fields = post_answer2string_disabled_entries(request)
        event.save()
        return redirect("event_overview")
    fields = string_disabled_entries2field_activation_entries(event.disabled_fields)
    return render(request, "events/event/field_activation.html", 
            {'request_user': request.user, 'event': event, 'fields': fields})


@cache_page(10) # Hold view in cache for 15 seconds
@xframe_options_exempt
def lecture_current_running(request, event_id, room_id):
    event = Event.objects.filter(id=event_id)
    if not event.exists():
        return HttpResponseBadRequest()
    event = event[0]

    room = Room.objects.filter(id=room_id)
    if not room.exists():
        return HttpResponseBadRequest()
    room = room[0]


    lectures = Lecture.objects.filter(event_id=event.id).filter(scheduled_in_room_id=room.id)

    now = timezone.now()

    found_lecture = None

    for lecture in lectures:
        if lecture.scheduled_presentation_time == "" or lecture.scheduled_presentation_time == 0:
            continue
        start = lecture.scheduled_presentation_time
        end = lecture.scheduled_presentation_time + timedelta(minutes=lecture.scheduled_presentation_length)
        if start <= now <= end:
            found_lecture = lecture
            break

    return render(request, "events/lecture/public/current_running.html", {'lecture': found_lecture, 'event': event, 'automatic_refresh': 10})
