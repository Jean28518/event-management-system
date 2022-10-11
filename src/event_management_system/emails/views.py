from ast import keyword
import os
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect, Http404, HttpResponseBadRequest
from events.models import Lecture
from .forms import EmailForm, EmailSendMassFormLecture, EmailSendMassFormUser
from .models import Email, MAIL_RECEIVER
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from event_management_system.meta import meta
from django.template.defaultfilters import date as _date

from django.core.mail import send_mail


@permission_required("emails.view_email")
def email_overview(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/users/login/")

    return render(request, "emails/overview.html", {'request_user': request.user, 'emails':Email.objects.all()})


@permission_required("emails.add_email")
def email_create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/users/login/")

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = Email()
            email.name = request.POST['name']
            email.subject = request.POST['subject']
            # email.answer_to_email = request.POST['answer_to_email']
            email.body = request.POST['body']
            email.save()
            return HttpResponseRedirect('/emails/')
    else:
        form = EmailForm()
        keywords = {}
        keywords['user'] = meta.get_fields_user()
        keywords['lecture'] = meta.get_fields_lecture()
        keywords['attendant'] = meta.get_fields_attendant()
        keywords['event'] = meta.get_fields_event()
        keywords['room'] = meta.get_fields_room()
        return render(request, 'emails/create.html', {'request_user': request.user, 'form': form, 'keywords': keywords})


@permission_required("emails.delete_email")
def email_delete(request, email_id):
    if Email.objects.filter(id=email_id).exists(): 
        Email.objects.filter(id=email_id).delete() 
    return HttpResponseRedirect("/emails/")


@permission_required("emails.change_email")
def email_edit(request, email_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/users/login/")

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = Email.objects.get(id=email_id)
            email.name = request.POST['name']
            email.subject = request.POST['subject']
            # email.answer_to_email = request.POST['answer_to_email']
            email.body = request.POST['body']
            email.save()
            return HttpResponseRedirect('/emails/')
    else:
        email = Email.objects.get(id=email_id)
        form = EmailForm(initial=email.__dict__)
        keywords = {}
        keywords['user'] = meta.get_fields_user()
        keywords['lecture'] = meta.get_fields_lecture()
        keywords['attendant'] = meta.get_fields_attendant()
        keywords['event'] = meta.get_fields_event()
        keywords['room'] = meta.get_fields_room()
        return render(request, 'emails/edit.html', {'request_user': request.user, 'form': form, 'email': email, 'keywords': keywords})


## Email Mass Sending depending at Users
class UserSelect:
    id = -1
    name = ""
    email = ""
    selected = False

    def __str__(self):
        return f"{self.id} {self.email} {self.selected}"

def get_user_select():
    users = User.objects.all().select_related("profile")
    return_value = []
    for user in users:
        user_select = UserSelect()
        user_select.id = user.id
        user_select.name = f"{user.first_name} {user.last_name} {user.profile.company}"
        user_select.email = user.email
        return_value.append(user_select)
    return return_value


@permission_required("emails.view_email")
def email_send_mass_user(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/users/login/")

    if request.method == 'POST':
        return _handle_email_send_mass_user_post_request(request)
    else:
        user_selections = get_user_select()
        form = EmailSendMassFormUser()
        return render(request, 'emails/send_mass_user.html', {'request_user': request.user, 'user_selections': user_selections, 'form': form})


def _handle_email_send_mass_user_post_request(request):
    user_selections = get_user_select()
    users = []
    for user_selection in user_selections:
        if f"{user_selection.id}" in request.POST:
            user_selection.selected = True
            users.append(User.objects.get(id=user_selection.id))
    
    email_to_send = Email.objects.get(id=request.POST['email'])

    for user in users:
        send_mail(get_converted_string_user(email_to_send.subject, user),
        get_converted_string_user(email_to_send.body, user),
        os.getenv("EMAIL_HOST_USER"),
        [user.email],
        fail_silently=False,)   
    
    return HttpResponseRedirect('/emails/')


@permission_required("emails.view_email")
def email_send_mass_user_select_all(request):
    if request.method == "POST":
        return _handle_email_send_mass_user_post_request(request)
    else:
        user_selections = get_user_select()
        for user_selection in user_selections:
            user_selection.selected = True

        form = EmailSendMassFormUser()
        return render(request, 'emails/send_mass_user.html', {'request_user': request.user, 'user_selections': user_selections, 'form': form})
      

@permission_required("emails.view_email")
def email_send_mass_user_deselect_all(request):
    if request.method == "POST":
        return _handle_email_send_mass_user_post_request(request)
    else:
        return email_send_mass_user(request)



## Email Mass Sending depending at Lectures
class LectureSelect:
    id = -1
    name = ""
    selected = False

    def __str__(self):
        return f"{self.id} {self.selected}"

def get_lecture_select(event_id):
    lectures = Lecture.objects.all().filter(event=event_id)
    return_value = []
    for lecture in lectures:
        lecture_select = LectureSelect()
        lecture_select.id = lecture.id
        lecture_select.name = f"{lecture.title}"
        return_value.append(lecture_select)
    return return_value


@permission_required("emails.view_email")
def email_send_mass_lecture(request, event_id, select_all=False):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/users/login/")

    if request.method == 'POST':
        lecture_selections = get_lecture_select(event_id)
        lectures_to_send = []
        for lecture_selection in lecture_selections:
            if f"{lecture_selection.id}" in request.POST:
                lecture_selection.selected = True
                lectures_to_send.append(Lecture.objects.get(id=lecture_selection.id))
        
        email_to_send = Email.objects.get(id=request.POST['email'])
        mail_receiver = request.POST['mail_receiver']
        
        
        email_adresses_with_lectures = []
        if mail_receiver == "PR":
            for lecture in lectures_to_send:
                user = lecture.presentator
                email_adresses_with_lectures.append((user.email, lecture))
        elif mail_receiver == "AT":
            for lecture in lectures_to_send:
                user = lecture.attendant
                if user:
                    email_adresses_with_lectures.append((user.email, lecture))
                else:
                    print(f"Attendant not set for lecture {lecture.title}. Not sending email.")


        for email_adress_with_lecture in email_adresses_with_lectures:
            send_mail(get_converted_string_lecture(email_to_send.subject, email_adress_with_lecture[1]),
            get_converted_string_lecture(email_to_send.body, email_adress_with_lecture[1]),
            os.getenv("EMAIL_HOST_USER"),
            [email_adress_with_lecture[0]],
            fail_silently=False,)   
        return HttpResponseRedirect(f"/events/{event_id}/lecture/overview/")
    else:
        lecture_selections = get_lecture_select(event_id)
        form = EmailSendMassFormLecture()
        if select_all:
            for lecture_selection in lecture_selections:
                lecture_selection.selected = True
        return render(request, 'emails/send_mass_lecture.html', {'request_user': request.user, 'lecture_selections': lecture_selections, 'form': form, "event_id": event_id})


@permission_required("emails.view_email")
def email_send_mass_lecture_select_all(request, event_id):
    select_all = False
    if request.method == "GET":
        select_all = True
    return email_send_mass_lecture(request, event_id, select_all=select_all)

@permission_required("emails.view_email")
def email_send_mass_lecture_deselect_all(request, event_id):
    return email_send_mass_lecture(request, event_id)



def get_converted_string_user(string, user):
    for keyword in meta.get_all_fields():
        if keyword.startswith("$user."):
            if keyword.startswith("$user.profile."):
                string = string.replace(keyword, str(user.profile.__dict__[keyword.replace("$user.profile.", "")]))
            else:
                string = string.replace(keyword, str(user.__dict__[keyword.replace("$user.", "")]))
    return string

def get_converted_string_lecture(string, lecture):
    user = lecture.presentator
    attendant = lecture.attendant
    room = lecture.scheduled_in_room
    event = lecture.event

    for keyword in meta.get_all_fields():
        if keyword.startswith("$user."):
            if keyword.startswith("$user.profile."):
                string = string.replace(keyword, str(user.profile.__dict__[keyword.replace("$user.profile.", "")]))
            else:
                string = string.replace(keyword, str(user.__dict__[keyword.replace("$user.", "")]))
        if keyword.startswith("$lecture."):
            if keyword == "$lecture.scheduled_presentation_time":
                string = string.replace(keyword, _date(lecture.__dict__[keyword.replace("$lecture.", "")], "l, j. F o, H:i"))
            string = string.replace(keyword, str(lecture.__dict__[keyword.replace("$lecture.", "")]))
        if keyword.startswith("$attendant.") and attendant:
            if keyword.startswith("$attendant.profile."):
                string = string.replace(keyword, str(user.profile.__dict__[keyword.replace("$attendant.profile.", "")]))
            else:
                string = string.replace(keyword, str(user.__dict__[keyword.replace("$attendant.", "")]))
        if keyword.startswith("$room.") and room:
            string = string.replace(keyword, str(room.__dict__[keyword.replace("$room.", "")]))
        if keyword.startswith("$event."):
            string = string.replace(keyword, str(event.__dict__[keyword.replace("$event.", "")]))

    return string