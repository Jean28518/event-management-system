from django import forms

class CreateForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    year = forms.CharField(label='Year', max_length=100, widget=forms.NumberInput(attrs={'class': "form-control"}))
    website = forms.CharField(label='Website', max_length=100, widget=forms.URLInput(attrs={'class': "form-control"}), required=False)

class EditForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    year = forms.CharField(label='Year', max_length=100, widget=forms.NumberInput(attrs={'class': "form-control"}))
    website = forms.CharField(label='Website', max_length=100, widget=forms.URLInput(attrs={'class': "form-control"}), required=False)
