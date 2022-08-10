from cProfile import label
from django import forms
from django.contrib.postgres.forms import SimpleArrayField


class CreateEventForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    year = forms.CharField(label='Year', max_length=100, widget=forms.NumberInput(attrs={'class': "form-control"}))
    website = forms.CharField(label='Website', max_length=100, widget=forms.URLInput(attrs={'class': "form-control"}), required=False)

class EditEventForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    year = forms.CharField(label='Year', max_length=100, widget=forms.NumberInput(attrs={'class': "form-control"}))
    website = forms.CharField(label='Website', max_length=100, widget=forms.URLInput(attrs={'class': "form-control"}), required=False)

class CreateRoomForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    website = forms.CharField(label='Website', max_length=100, widget=forms.URLInput(attrs={'class': "form-control"}), required=False)
    coordinates = forms.CharField(label='Coordinates', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}), required=False)

class EditRoomForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    website = forms.CharField(label='Website', max_length=100, widget=forms.URLInput(attrs={'class': "form-control"}), required=False)
    coordinates = forms.CharField(label='Coordinates', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}), required=False)
