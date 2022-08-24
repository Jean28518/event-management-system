from django import forms

from .models import MAIL_RECEIVER, Email

class EmailForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    subject = forms.CharField(label='Subject', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    # answer_to_email = forms.CharField(label='Answer to email adress', max_length=100, widget=forms.EmailInput(attrs={'class': "form-control"}))
    body = forms.CharField(label='Body', max_length=8192, widget=forms.Textarea(attrs={'class': "form-control"}))

class EmailSendMassFormUser(forms.Form):
    email = forms.ModelChoiceField(label="Email", queryset=Email.objects.all(), widget=forms.Select(attrs={'class': "form-select"}), required=True, blank=False)

class EmailSendMassFormLecture(forms.Form):
    email = forms.ModelChoiceField(label="Email", queryset=Email.objects.all(), widget=forms.Select(attrs={'class': "form-select"}), required=True, blank=False)
    mail_receiver = forms.CharField(label='Mail Receivers', widget=forms.Select(choices=MAIL_RECEIVER, attrs={'class': "form-control"}))