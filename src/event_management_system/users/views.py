from urllib import request
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .authentication import get_user, handle_failed_authorization
from .models import Profile
from django.core import serializers
from django.contrib.auth.models import User, make_password, Group
from django.contrib.auth import authenticate, login, logout
from .forms import CreateForm, EditForm, LoginForm, RegisterForm, ROLES
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
import random




def user_reset_password(request, user_id):
    if Profile.objects.filter(id=user_id).exists():
        user = User.objects.select_related('profile').filter(id=user_id)[0]      
        user.profile.reset_password()
        return HttpResponseRedirect(f"/users/edit/{user_id}?pwreset=success")

    return HttpResponse("User not found.")


@permission_required('users.view_profile') 
def user_overview(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/users/login/")
    print(request.user._meta.fields)
    users = User.objects.all().select_related('profile')
    for user in users:
        user.user_role = _get_user_role(user)
        if user.user_role == "CO":
            user.user_role = ROLES[0][1]
        if user.user_role == "AT":
            user.user_role = ROLES[1][1]
        if user.user_role == "OR":
            user.user_role = ROLES[2][1]
        if user.user_role == "AD":
            user.user_role = ROLES[3][1]
        print(_get_user_role(user))
    return render(request, "users/overview.html", {'request_user': request.user, 'users': users})

@permission_required('users.delete_profile') 
def user_delete(request, user_id):
    if User.objects.filter(id=user_id).exists(): 
        User.objects.filter(id=user_id).delete() 
        print("Deleted")
    return HttpResponseRedirect("/users/")

@permission_required('users.add_profile') 
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
            elif request.POST['user_role'] == 'AD' and request.user.groups.filter(name="Administrator").exists():
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

        form = CreateForm(initial = {'private_pin': _get_random_private_pin()})
        return render(request, 'users/create.html', {'request_user': request.user, 'form': form})

def _get_random_private_pin():
    # 10000 lowest Pin
    # 99999 highest Pin
    num = int((random.random()*89999) + 10000)
    print(num)
    return num

def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User()
            user.username = request.POST['email']
            user.email = request.POST['email']
            user.last_name = request.POST['last_name']
            user.first_name = request.POST['first_name']
            user.password = make_password(request.POST['password'])
            user.save()

            # Add user to group Contact
            group = Group.objects.get(name='Contact')
            group.user_set.add(user)
          
            profile = user.profile
            profile.website = request.POST['website']
            profile.company = request.POST['company']
            profile.over_18 = (request.POST.get('over_18', "off") == "on")
            profile.save()
            return HttpResponseRedirect('/lectures/public/create/')
    else:
        form = RegisterForm()
        return render(request, 'users/create_public.html', {'form': form})

@permission_required('users.change_profile') 
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


            # TODO: This should only be possible by admins
            print(request.POST['user_role'])
            if request.POST['user_role'] == 'CO':
                user.groups.clear()
                group = Group.objects.get(name='Contact')
                group.user_set.add(user)
                print("DONE")
            elif request.POST['user_role'] == 'AT':
                user.groups.clear()
                group = Group.objects.get(name='Attendant')
                group.user_set.add(user)
            elif request.POST['user_role'] == 'OR':
                user.groups.clear()
                group = Group.objects.get(name='Organisator')
                group.user_set.add(user)
            elif request.POST['user_role'] == 'AD' and request.user.groups.filter(name="Administrator").exists():
                user.groups.clear()
                group = Group.objects.get(name='Administrator')
                group.user_set.add(user)
            
            profile.save()
            return HttpResponseRedirect('/users/')
        return HttpResponseServerError()
    else:
        user = User.objects.select_related('profile').filter(id=user_id)[0]
        

        dict = {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'password': user.password,
            'website': user.profile.website,
            'company': user.profile.company,
            'over_18': user.profile.over_18 == True,
            'private_pin': user.profile.private_pin,
            'user_role': _get_user_role(user)
        }

        pwreset = ""
        if 'pwreset' in request.GET:
            pwreset = request.GET['pwreset']#

        

        form = EditForm(initial=dict)
        print(form.__dict__['fields']['over_18'].__dict__)
        return render(request, 'users/edit.html', {'request_user': request.user, 'form': form, 'pwreset': pwreset, 'user': user})

def _get_user_role(user):
    user_role = "CO"
    if user.groups.filter(name='Contact').exists():
        user_role = "CO"
    elif user.groups.filter(name='Attendant').exists():
        user_role = "AT"
    elif user.groups.filter(name='Organisator').exists():
        user_role = "OR"
    elif user.groups.filter(name='Administrator').exists():
        user_role = "AD"
    return user_role

def user_login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['email'], password=request.POST['password'])
        if user and user.is_authenticated:
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