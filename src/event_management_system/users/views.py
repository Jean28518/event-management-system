from urllib import request
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .authentication import get_user, handle_failed_authorization
from .models import Profile
from django.core import serializers
from django.contrib.auth.models import User, make_password, Group
from django.contrib.auth import authenticate, login, logout
from .forms import CreateForm, EditForm, LoginForm, RegisterForm, PasswordForgot, PasswordChange, ROLES
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
import random
from django.core.mail import send_mail
from django.utils.translation import gettext as _
from django.utils.translation import get_language

def user_reset_password(request):
    if request.method == "POST":
        form = PasswordForgot(request.POST)
        if form.is_valid():
            email = request.POST['email']
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)      
                password = user.profile.reset_password()
                send_mail(subject="New Password", from_email="", message=f"Your new password is:\n\n{password}", recipient_list=[user.email])
            return render(request, "users/reset_password.html", {'mail_sent': True, 'form': form})
    else:
        form = PasswordForgot()
        return render(request, "users/reset_password.html", {'mail_sent': False, 'form': form})

@login_required
def user_change_password(request):
    if request.method == "POST":
        form = PasswordChange(request.POST)
        if form.is_valid():
            user = request.user
            authenticated_user = authenticate(username=user.username, password=request.POST['old_password'])
            if authenticated_user and authenticated_user.is_authenticated:
                if len(request.POST['new_password']) >= 8:
                    if request.POST['new_password'] == request.POST['new_password_repeated']:
                        user.set_password(request.POST['new_password'])
                        return render(request, "users/change_password.html", 
                            {
                                'request_user': request.user,
                                'success': True, 
                                'wrong_password': False, 
                                'passwords_differ': False, 
                                'password_to_short': False, 
                                'form': PasswordChange()
                            })
                    else:
                        # Passwords differ
                        return render(request, "users/change_password.html", 
                                {
                                    'request_user': request.user,
                                    'success': False, 
                                    'wrong_password': False, 
                                    'passwords_differ': True, 
                                    'password_to_short': False, 
                                    'form': form
                                })
                else:
                    ## Password length under 8
                    return render(request, "users/change_password.html", 
                            {
                                'request_user': request.user,
                                'success': False, 
                                'wrong_password': False, 
                                'passwords_differ': False, 
                                'password_to_short': True, 
                                'form': form
                            })
            else:
                return render(request, "users/change_password.html", 
                            {
                                'request_user': request.user,
                                'success': False, 
                                'wrong_password': True, 
                                'passwords_differ': False, 
                                'password_to_short': False, 
                                'form': form
                            })

           
    else:
        form = PasswordChange()
        return render(request, "users/change_password.html", 
                            {
                                'request_user': request.user,
                                'success': False, 
                                'wrong_password': False, 
                                'passwords_differ': False, 
                                'password_to_short': False, 
                                'form': form
                            })

        


def user_overview(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/users/login/")
    if not request.user.has_perm('users.view_profile'):
        return HttpResponseRedirect("/")
    print(_("Users"))
    print(get_language())
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
            if User.objects.filter(email=request.POST['email']).exists():
                return render(request, 'users/create.html', {'request_user': request.user, 'form': form, 'email_already_exists': True})
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
        return render(request, 'users/create.html', {'request_user': request.user, 'form': form, 'email_already_exists': False})

def _get_random_private_pin():
    # 10000 lowest Pin
    # 99999 highest Pin
    num = int((random.random()*89999) + 10000)
    print(num)
    return num

def user_register(request, next = ''):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print(request.GET)
            if User.objects.filter(email=request.POST['email']).exists():
                return render(request, 'users/create_public.html', {'form': form, 'email_already_exists': True})
            user = User()
            user.username = request.POST['email']
            user.email = request.POST['email']
            user.last_name = request.POST['last_name']
            user.first_name = request.POST['first_name']
            user.password = make_password(request.POST['password'])
            user.save()

            # Add user to group Contact. Add first user to Group Administrator
            if User.objects.count() == 1:
                group = Group.objects.get(name='Administrator')
                user.is_staff = True
                user.save()
            else:
                group = Group.objects.get(name='Contact')
            group.user_set.add(user)
          
            profile = user.profile
            profile.website = request.POST['website']
            profile.company = request.POST['company']
            profile.over_18 = (request.POST.get('over_18', "off") == "on")
            profile.save()
            login(request, user)
            if request.GET.get("next", "") != "":
                return HttpResponseRedirect(request.GET['next'])
            else: 
                return HttpResponseRedirect('/')
            
    else:
        form = RegisterForm()
        return render(request, 'users/create_public.html', {'form': form, 'email_already_exists': False})

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
                group = Group.objects.get(name=_("Administrator"))
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
        return render(request, 'users/edit.html', {'request_user': request.user, 'form': form, 'pwreset': pwreset, 'user': user})


@permission_required('users.view_profile') 
def user_view(request, user_id):
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

    form = EditForm(initial=dict)
    for field in form.fields:
        form.fields[field].disabled = True
    return render(request, 'users/view.html', {'request_user': request.user, 'form': form, 'user': user})

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
            if request.GET.get("next", "") != "":
                return HttpResponseRedirect(request.GET['next'])
            else: 
                return HttpResponseRedirect('/')
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
