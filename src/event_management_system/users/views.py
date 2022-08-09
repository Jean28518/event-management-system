from urllib import request
from django.http import HttpResponse, HttpResponseServerError, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .authentication import get_user, handle_failed_authorization
from .models import Profile
from django.core import serializers
from django.contrib.auth.models import User, make_password, Group
from django.contrib.auth import authenticate, login, logout
from .forms import CreateForm, EditForm, LoginForm
from django.contrib.auth.decorators import login_required


@csrf_exempt 
def api_create(request):
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
def api_update(request):
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
def api_change_password(request):
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
def api_delete(request):
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

def api_get(request):
    user = get_user(request)
    if type(user) != User: 
        return handle_failed_authorization(user)

    if request.method == 'GET':
        data = serializers.serialize("json", User.objects.all().select_related('profile'))
        return HttpResponse(data)
    return HttpResponse("wrong http method.")

@csrf_exempt 
def api_reset_password(request):
    if request.method == "POST":
        if not Profile.objects.filter(email=request.POST['email']).exists():
            return HttpResponse("user not found.")
        user = Profile.objects.get(email=request.POST['email'])
        user.reset_password()
        return HttpResponse("success.")

    return HttpResponse("wrong http method.")

def user_reset_password(request, user_id):
    if Profile.objects.filter(id=user_id).exists():
        user = User.objects.select_related('profile').filter(id=user_id)[0]      
        user.set_password("12341234")
        return HttpResponseRedirect(f"/users/edit/{user_id}?pwreset=success")

    return HttpResponse("User not found.")


def user_overview(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/users/login/")
    
    return render(request, "users/overview.html", {'users':User.objects.all().select_related('profile')})

def user_delete(request, user_id):
    if User.objects.filter(id=user_id).exists(): 
        User.objects.filter(id=user_id).delete() 
        print("Deleted")
    return HttpResponseRedirect("/users/")

def user_create(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            user = User()
            user.username = request.POST['email']
            user.email = request.POST['email']
            user.last_name = request.POST['last_name']
            user.first_name = request.POST['first_name']
            user.password = make_password(request.POST['password'])
            user.save()

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


            profile = user.profile
            profile.website = request.POST['website']
            profile.company = request.POST['company']
            profile.over_18 = (request.POST.get('over_18', "off") == "on")
            profile.private_pin = request.POST['private_pin']
            profile.save()
            return HttpResponseRedirect('/users/')
    else:
        form = CreateForm()
        return render(request, 'users/create.html', {'form': form})

def user_edit(request, user_id):
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            user = User.objects.select_related('profile').filter(id=user_id)[0]
            user.username = request.POST['email']
            user.email = request.POST['email']
            user.last_name = request.POST['last_name']
            user.first_name = request.POST['first_name']
            user.save()

            profile = user.profile
            profile.website = request.POST['website']
            profile.company = request.POST['company']
            profile.over_18 = (request.POST.get('over_18', "off") == "on")
            profile.private_pin = request.POST['private_pin']


            user.groups.clear()
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
            return HttpResponseRedirect('/users/')
        return HttpResponseServerError()
    else:
        user = User.objects.select_related('profile').filter(id=user_id)[0]
        user_role = "CO"
        if user.groups.filter(name='Contact').exists():
            user_role = "CO"
        elif user.groups.filter(name='Attendant').exists():
            user_role = "AT"
        elif user.groups.filter(name='Organisator').exists():
            user_role = "OR"
        elif user.groups.filter(name='Administrator').exists():
            user_role = "AD"

        dict = {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'password': user.password,
            'website': user.profile.website,
            'company': user.profile.company,
            'over_18': user.profile.over_18 == True,
            'private_pin': user.profile.private_pin,
            'user_role': user_role

        }

        pwreset = ""
        if 'pwreset' in request.GET:
            pwreset = request.GET['pwreset']

        form = EditForm(initial=dict)
        return render(request, 'users/edit.html', {'form': form, 'pwreset': pwreset})

def user_login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['email'], password=request.POST['password'])
        if user.is_authenticated:
            login(request, user)
            return HttpResponseRedirect("/users/")
        else:
            form = LoginForm()
            return render(request, 'users/login.html', {'form': form, 'login_failed': True})
    else:
        if request.user is not None:
            form = LoginForm()
            return render(request, 'users/login.html', {'form': form, 'login_failed': False})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/users/login/")