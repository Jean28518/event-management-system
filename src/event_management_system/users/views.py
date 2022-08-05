from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import User
from django.core import serializers



# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the user index.")

# TODO: remove csrf exempt
@csrf_exempt 
def create(request):
    if request.method == 'POST':
        user = User()
        user.email = request.POST['email']
        user.surname = request.POST['surname']
        user.name = request.POST['name']
        user.website = request.POST['website']
        user.company = request.POST['company']
        user.over_18 = request.POST['over_18'] == "true"
        user.password = request.POST['password']
        user.private_pin = request.POST['private_pin']
        
        user.user_role = User.getUserRoleOfString(request.POST['user_role'])

        user.save()
    return HttpResponse("success.")

# TODO: remove csrf exempt
@csrf_exempt 
def update(request):
    if request.method == 'POST':
        if not User.objects.filter(email=request.POST['email']).exists():
            return HttpResponse("user not found.")
        user = User.objects.get(email=request.POST['email'])

        if request.POST.__contains__('new_email'):
            user.email = request.POST['new_email']
        user.surname = request.POST['surname']
        user.name = request.POST['name']
        user.website = request.POST['website']
        user.company = request.POST['company']
        user.over_18 = request.POST['over_18'] == "true"
        user.password = request.POST['password']
        user.private_pin = request.POST['private_pin']

        # TODO: This should only be possible by admins
        user.user_role = User.getUserRoleOfString(request.POST['user_role'])
        
        user.save()
    return HttpResponse("success.")

# TODO: remove csrf exempt
@csrf_exempt 
def delete(request):
    if request.method == 'POST':
        if User.objects.filter(email=request.POST['email']).exists(): 
            User.objects.filter(email=request.POST['email']).delete() 
            return HttpResponse("success.")
        else:
            return HttpResponse("Email not found.")
        
    return HttpResponse("wrong http method.")

# TODO: remove csrf exempt
@csrf_exempt 
def get(request):
    if request.method == 'GET':
        data = serializers.serialize("json", User.objects.all())
        return HttpResponse(data)
    return HttpResponse("wrong http method.")

@csrf_exempt 
def reset_password(request):
    if request.method == "POST":
        if not User.objects.filter(email=request.POST['email']).exists():
            return HttpResponse("user not found.")
        user = User.objects.get(email=request.POST['email'])
        user.reset_password()
        return HttpResponse("success.")

    return HttpResponse("wrong http method.")