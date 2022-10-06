from django import forms
from django.utils.translation import gettext_lazy as _


ROLES = [
    ('CO', _('Contact')),
    ('AT', _('Attendant')),
    ('OR', _('Organisator')),
    ('AD', _('Administrator')),
    ]

class UserForm(forms.Form):
    user_role= forms.CharField(label=_('Role'), widget=forms.Select(choices=ROLES, attrs={'class': "form-control"}))
    email = forms.CharField(label=_('Email'), max_length=100, widget=forms.EmailInput(attrs={'class': "form-control"}))
    first_name = forms.CharField(label=_('First name'), max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}),)
    last_name = forms.CharField(label=_('Last name'), max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}),)
    password = forms.CharField(label=_('Password'), max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}),)
    website = forms.CharField(label=_('Website'), max_length=100, widget=forms.URLInput(attrs={'class': "form-control"}), required=False)
    company = forms.CharField(label=_('Company'), max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}), required=False)
    over_18 = forms.BooleanField(label=_('Over 18'), widget=forms.CheckboxInput(attrs={'class': "form-check-input"}), required=False)
    private_pin = forms.CharField(label=_('Private Pin'), max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}), required=False)

# Public Contact Creation (Creates automatically contact)
class RegisterForm(forms.Form):
    email = forms.CharField(label=_('Email'), max_length=100, widget=forms.EmailInput(attrs={'class': "form-control"}))
    first_name = forms.CharField(label=_('First name'), max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}),)
    last_name = forms.CharField(label=_('Last name'), max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}),)
    password = forms.CharField(label=_('Password'), max_length=100, widget=forms.PasswordInput(attrs={'class': "form-control"}),)
    website = forms.CharField(label=_('Website'), max_length=100, widget=forms.URLInput(attrs={'class': "form-control"}), required=False)
    company = forms.CharField(label=_('Company'), max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}), required=False)
    over_18 = forms.BooleanField(label=_('Over 18'), widget=forms.CheckboxInput(attrs={'class': "form-check-input"}), required=False)
    
class LoginForm(forms.Form):
    email = forms.CharField(label=_('Email'), max_length=100, widget=forms.EmailInput(attrs={'class': "form-control"}))
    password = forms.CharField(label=_('Password'), max_length=100, widget=forms.PasswordInput(attrs={'class': "form-control"}),)
    
class PasswordForgot(forms.Form):
    email = forms.CharField(label=_('Email'), max_length=100, widget=forms.EmailInput(attrs={'class': "form-control"}))

class PasswordChange(forms.Form):
    old_password = forms.CharField(label=_('Old Password'), max_length=100, widget=forms.PasswordInput(attrs={'class': "form-control"}),)
    new_password = forms.CharField(label=_('New Password'), max_length=100, widget=forms.PasswordInput(attrs={'class': "form-control"}),)
    new_password_repeated = forms.CharField(label=_('New Password (repeated)'), max_length=100, widget=forms.PasswordInput(attrs={'class': "form-control"}),)

