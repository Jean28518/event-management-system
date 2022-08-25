from django import forms

ROLES = [
    ('CO', 'Contact'),
    ('AT', 'Attendant'),
    ('OR', 'Organisator'),
    ('AD', 'Admin'),
    ]

class CreateForm(forms.Form):
    user_role= forms.CharField(label='Role', widget=forms.Select(choices=ROLES, attrs={'class': "form-control"}))
    email = forms.CharField(label='Email', max_length=100, widget=forms.EmailInput(attrs={'class': "form-control"}))
    first_name = forms.CharField(label='First name', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}),)
    last_name = forms.CharField(label='Last name', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}),)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput(attrs={'class': "form-control"}),)
    website = forms.CharField(label='Website', max_length=100, widget=forms.URLInput(attrs={'class': "form-control"}), required=False)
    company = forms.CharField(label='Company', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}), required=False)
    over_18 = forms.BooleanField(label='Over 18', widget=forms.CheckboxInput(attrs={'class': "form-check-input"}), required=False)
    private_pin = forms.CharField(label='Private Pin', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}), required=False)

# Public Contact Creation (Creates automatically contact)
class RegisterForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100, widget=forms.EmailInput(attrs={'class': "form-control"}))
    first_name = forms.CharField(label='First name', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}),)
    last_name = forms.CharField(label='Last name', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}),)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput(attrs={'class': "form-control"}),)
    website = forms.CharField(label='Website', max_length=100, widget=forms.URLInput(attrs={'class': "form-control"}), required=False)
    company = forms.CharField(label='Company', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}), required=False)
    over_18 = forms.BooleanField(label='Over 18', widget=forms.CheckboxInput(attrs={'class': "form-check-input"}), required=False)

class EditForm(forms.Form):
    user_role= forms.CharField(label='Role', widget=forms.Select(choices=ROLES, attrs={'class': "form-control"}))
    email = forms.CharField(label='Email', max_length=100, widget=forms.EmailInput(attrs={'class': "form-control"}))
    first_name = forms.CharField(label='First name', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}),)
    last_name = forms.CharField(label='Last name', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}),)
    website = forms.CharField(label='Website', max_length=100, widget=forms.URLInput(attrs={'class': "form-control"}), required=False)
    company = forms.CharField(label='Company', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}), required=False)
    over_18 = forms.BooleanField(label='Over 18', widget=forms.CheckboxInput(attrs={'class': "form-check-input"}), required=False)
    private_pin = forms.CharField(label='Private Pin', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}), required=False)
    
class LoginForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100, widget=forms.EmailInput(attrs={'class': "form-control"}))
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput(attrs={'class': "form-control"}),)