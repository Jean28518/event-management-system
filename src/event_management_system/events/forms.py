from cProfile import label
from django import forms
from django.contrib.postgres.forms import SimpleArrayField

from .models import PRESENTATION_STYLE, TARGET_GROUP


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

class LoginForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100, widget=forms.EmailInput(attrs={'class': "form-control"}))
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput(attrs={'class': "form-control"}),)

class LectureSubmitForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}),)
    description = forms.CharField(label='Description (max. 2048 signs)', max_length=2048, widget=forms.Textarea(attrs={'class': "form-control"}),)
    target_group = forms.CharField(label='Target Group', widget=forms.Select(choices=TARGET_GROUP, attrs={'class': "form-control"}))
    qualification_for_lecture = forms.CharField(label='I am qualified for the presentatien beacause...', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}),)
    preferred_presentation_style = forms.CharField(label='Preferred presentation style', widget=forms.Select(choices=PRESENTATION_STYLE, attrs={'class': "form-control"}))
    questions_during_lecture = forms.BooleanField(label='Should questions during lectures been asked?', widget=forms.CheckboxInput(attrs={'class': "form-check-input"}), required=False)
    questions_after_lecture = forms.BooleanField(label='Should questions after lectures been asked?', widget=forms.CheckboxInput(attrs={'class': "form-check-input"}), required=False)
    minimal_lecture_length = forms.IntegerField(label='Minimal Lecture Length (in minutes)', widget=forms.NumberInput(attrs={'class': "form-control"}),)
    maximal_lecture_length = forms.IntegerField(label='Maximal Lecture Length (in minutes)', widget=forms.NumberInput(attrs={'class': "form-control"}),)
    additional_information_by_presentator = forms.CharField(label='Additional information (max. 2048 signs)', max_length=2048, widget=forms.Textarea(attrs={'class': "form-control"}),)
    related_website = forms.CharField(label='Lecture related Website', max_length=100, widget=forms.URLInput(attrs={'class': "form-control"}), required=False)
    
    # TODO Checklist for available Timeslots