from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect, Http404, HttpResponseBadRequest
from .forms import EmailForm
from .models import Email

def email_overview(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/users/login/")
    
    return render(request, "emails/overview.html", {'emails':Email.objects.all()})

def email_create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/users/login/")

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = Email()
            email.name = request.POST['name']
            email.subject = request.POST['subject']
            email.answer_to_email = request.POST['answer_to_email']
            email.body = request.POST['body']
            email.save()
            return HttpResponseRedirect('/emails/')
    else:
        form = EmailForm()
        return render(request, 'emails/create.html', {'form': form})

def email_delete(request, email_id):
    if Email.objects.filter(id=email_id).exists(): 
        Email.objects.filter(id=email_id).delete() 
    return HttpResponseRedirect("/emails/")

def email_edit(request, email_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/users/login/")

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = Email.objects.get(id=email_id)
            email.name = request.POST['name']
            email.subject = request.POST['subject']
            email.answer_to_email = request.POST['answer_to_email']
            email.body = request.POST['body']
            email.save()
            return HttpResponseRedirect('/emails/')
    else:
        email = Email.objects.get(id=email_id)
        form = EmailForm(initial=email.__dict__)
        return render(request, 'emails/edit.html', {'form': form, 'email': email})