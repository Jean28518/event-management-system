from django.utils.translation import gettext_lazy as _
from django import forms

ROLES = [
    ('CO', 'Contact'),
    ('AT', 'Attendant'),
    ('OR', 'Organisator'),
    ('AD', 'Admin'),
    ]


class CreateForm(forms.Form):
    user_role = forms.CharField(label=_("forms.user.create.role"), widget=forms.Select(choices=ROLES, attrs={'class': "form-control"}))
    email = forms.CharField(label=_("forms.user.create.email"), max_length=100, widget=forms.EmailInput(attrs={'class': "form-control"}))
    first_name = forms.CharField(label=_("forms.user.create.firstname"), max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}),)
    last_name = forms.CharField(label=_("forms.user.create.lastname"), max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}),)
    password = forms.CharField(label=_("forms.user.create.password"), max_length=100, widget=forms.PasswordInput(attrs={'class': "form-control"}),)
    website = forms.CharField(label=_("forms.user.create.website"), max_length=100, widget=forms.URLInput(attrs={'class': "form-control"}), required=False)
    company = forms.CharField(label=_("forms.user.create.company"), max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}), required=False)
    over_18 = forms.BooleanField(label=_("forms.user.create.adult"), widget=forms.CheckboxInput(attrs={'class': "form-check-input"}), required=False)
    private_pin = forms.CharField(label=_("forms.user.create.pin"), max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}), required=False)


# Public Contact Creation (Creates automatically contact)
class RegisterForm(forms.Form):
    email = forms.CharField(label=_("forms.user.register.email"), max_length=100, widget=forms.EmailInput(attrs={'class': "form-control"}))
    first_name = forms.CharField(label=_("forms.user.register.firstname"), max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}),)
    last_name = forms.CharField(label=_("forms.user.register.lastname"), max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}),)
    password = forms.CharField(label=_("forms.user.register.password"), max_length=100, widget=forms.PasswordInput(attrs={'class': "form-control"}),)
    website = forms.CharField(label=_("forms.user.register.website"), max_length=100, widget=forms.URLInput(attrs={'class': "form-control"}), required=False)
    company = forms.CharField(label=_("forms.user.register.company"), max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}), required=False)
    over_18 = forms.BooleanField(label=_("forms.user.register.adult"), widget=forms.CheckboxInput(attrs={'class': "form-check-input"}), required=False)


class EditForm(forms.Form):
    user_role = forms.CharField(label=_("forms.user.edit.role"), widget=forms.Select(choices=ROLES, attrs={'class': "form-control"}))
    email = forms.CharField(label=_("forms.user.edit.email"), max_length=100, widget=forms.EmailInput(attrs={'class': "form-control"}))
    first_name = forms.CharField(label=_("forms.user.edit.firstname"), max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}),)
    last_name = forms.CharField(label=_("forms.user.edit.lastname"), max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}),)
    website = forms.CharField(label=_("forms.user.edit.website"), max_length=100, widget=forms.URLInput(attrs={'class': "form-control"}), required=False)
    company = forms.CharField(label=_("forms.user.edit.company"), max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}), required=False)
    over_18 = forms.BooleanField(label=_("forms.user.edit.adult"), widget=forms.CheckboxInput(attrs={'class': "form-check-input"}), required=False)
    private_pin = forms.CharField(label=_("forms.user.edit.pin"), max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}), required=False)


class LoginForm(forms.Form):
    email = forms.CharField(label=_("forms.user.login.email"), max_length=100, widget=forms.EmailInput(attrs={'class': "form-control"}))
    password = forms.CharField(label=_("forms.user.login.password"), max_length=100, widget=forms.PasswordInput(attrs={'class': "form-control"}),)