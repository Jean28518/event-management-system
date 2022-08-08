from django.http import HttpResponse, HttpResponseServerError, HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .authentication import get_user, handle_failed_authorization
from .models import Profile
from django.core import serializers
from django.contrib.auth.models import User, make_password, Group
from django.contrib.auth import authenticate, login

@csrf_exempt 
def create(request):
    user = get_user(request)
    if type(user) != User: 
        return handle_failed_authorization(user)

    if request.method == 'POST':
        user = User()
        user.username = request.POST['email']
        user.email = request.POST['email']
        user.last_name = request.POST['surname']
        user.first_name = request.POST['name']
        user.password = make_password(request.POST['password'])
        user.save()

        profile = user.profile
        profile.website = request.POST['website']
        profile.company = request.POST['company']
        profile.over_18 = request.POST['over_18'] == "true"
        profile.private_pin = request.POST['private_pin']

        # TODO: This should only be possible by admins
        if request.POST['user_role'] == 'CO':
            group = Group.objects.get_or_create(name='Contact')[0]
            group.user_set.add(user)
        elif request.POST['user_role'] == 'AT':
            group = Group.objects.get_or_create(name='Attendant')[0]
            group.user_set.add(user)
        elif request.POST['user_role'] == 'OR':
            group = Group.objects.get_or_create(name='Organisator')[0]
            group.user_set.add(user)
        elif request.POST['user_role'] == 'AD':
            group = Group.objects.get_or_create(name='Administrator')[0]
            group.user_set.add(user)
        
        profile.save()
    return HttpResponse("success.")

@csrf_exempt 
def update(request):
    user = get_user(request)
    if type(user) != User: 
        return handle_failed_authorization(user)

    if request.method == 'POST':
        if not User.objects.filter(username=request.POST['email']).exists():
            return HttpResponse("user not found.")
        user = User.objects.get(username=request.POST['email'])
        user.username = request.POST['email']
        user.email = request.POST['email']
        user.last_name = request.POST['surname']
        user.first_name = request.POST['name']
        user.save()

        profile = user.profile
        profile.website = request.POST['website']
        profile.company = request.POST['company']
        profile.over_18 = request.POST['over_18'] == "true"
        profile.private_pin = request.POST['private_pin']


        if Group.objects.get_or_create(name='Contact')[0].user_set.filter(username=request.POST['email']).exists():
            Group.objects.get(name='Contact').user_set.remove(user)
        if Group.objects.get_or_create(name='Attendant')[0].user_set.filter(username=request.POST['email']).exists():
            Group.objects.get(name='Attendant').user_set.remove(user)
        if Group.objects.get_or_create(name='Organisator')[0].user_set.filter(username=request.POST['email']).exists():
            Group.objects.get(name='Organisator').user_set.remove(user)
        if Group.objects.get_or_create(name='Administrator')[0].user_set.filter(username=request.POST['email']).exists():
            Group.objects.get(name='Administrator').user_set.remove(user)

        

        # TODO: This should only be possible by admins
        if request.POST['user_role'] == 'CO':
            group = Group.objects.get(name='Contact')
            group.user_set.add(user)
        elif request.POST['user_role'] == 'AT':
            group = Group.objects.get(name='Attendant')
            group.user_set.add(user)
        elif request.POST['user_role'] == 'OR':
            group = Group.objects.get(name='Organisator')
            group.user_set.add(user)
        elif request.POST['user_role'] == 'AD':
            group = Group.objects.get(name='Administrator')
            group.user_set.add(user)
        
        profile.save()
        return HttpResponse("success.")
    return HttpResponse("wrong http method.")

@csrf_exempt 
def change_password(request):
    user = get_user(request)
    if type(user) != User: 
        return handle_failed_authorization(user)

    if request.method == 'POST':
        if not User.objects.filter(username=request.POST['email']).exists():
            return HttpResponse("user not found.")
        user = User.objects.get(username=request.POST['email'])
        user.password = make_password(request.POST['password'])
        user.save()
        return HttpResponse("success.")
    return HttpResponse("wrong http method.")

@csrf_exempt
def delete(request):
    user = get_user(request)
    if type(user) != User: 
        return handle_failed_authorization(user)

    if request.method == 'POST':
        if Profile.objects.filter(email=request.POST['email']).exists(): 
            Profile.objects.filter(email=request.POST['email']).delete() 
            return HttpResponse("success.")
        else:
            return HttpResponse("Email not found.")
        
    return HttpResponse("wrong http method.")

def get(request):
    user = get_user(request)
    if type(user) != User: 
        return handle_failed_authorization(user)

    if request.method == 'GET':
        data = serializers.serialize("json", User.objects.all().select_related('profile'))
        return HttpResponse(data)
    return HttpResponse("wrong http method.")

@csrf_exempt 
def reset_password(request):
    if request.method == "POST":
        if not Profile.objects.filter(email=request.POST['email']).exists():
            return HttpResponse("user not found.")
        user = Profile.objects.get(email=request.POST['email'])
        user.reset_password()
        return HttpResponse("success.")

    return HttpResponse("wrong http method.")