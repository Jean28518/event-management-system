from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.models import User


from .models import PRESENTATION_STYLE, TARGET_GROUP, Event, Room


class EventForm(forms.Form):
    name = forms.CharField(label=_("forms.event.name"), max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    year = forms.CharField(label=_("forms.event.year"), max_length=100, widget=forms.NumberInput(attrs={'class': "form-control"}))
    website = forms.CharField(
        label=_("forms.event.website"), max_length=100,
        widget=forms.URLInput(attrs={'class': "form-control"}),
        required=False
    )


class RoomFrom(forms.Form):
    name = forms.CharField(label=_("forms.room.name"), max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    website = forms.CharField(
        label=_("forms.room.website"), max_length=100,
        widget=forms.URLInput(attrs={'class': "form-control"}),
        required=False
    )
    coordinates = forms.CharField(
        label=_("forms.room.coordinates"), max_length=100,
        widget=forms.TextInput(attrs={'class': "form-control"}),
        required=False
    )


class LoginForm(forms.Form):
    email = forms.CharField(label=_("forms.login.email"), max_length=100, widget=forms.EmailInput(attrs={'class': "form-control"}))
    password = forms.CharField(
        label=_("forms.login.password"), max_length=100,
        widget=forms.PasswordInput(attrs={'class': "form-control"}),
    )


class LectureSubmitForm(forms.Form):
    title = forms.CharField(label=_("forms.lecture.submit.titel"), max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}),)
    description = forms.CharField(label=_("forms.lecture.submit.description"), max_length=2048, widget=forms.Textarea(attrs={'class': "form-control"}),)
    target_group = forms.CharField(label=_("forms.lecture.submit.group"), widget=forms.Select(choices=TARGET_GROUP, attrs={'class': "form-control"}))
    qualification_for_lecture = forms.CharField(label=_("forms.lecture.submit.qualification"), max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}),)
    preferred_presentation_style = forms.CharField(label=_("forms.lecture.submit.style"), widget=forms.Select(choices=PRESENTATION_STYLE, attrs={'class': "form-select"}))
    questions_during_lecture = forms.BooleanField(label=_("forms.lecture.submit.questions.during"), widget=forms.CheckboxInput(attrs={'class': "form-check-input"}), required=False)
    questions_after_lecture = forms.BooleanField(label=_("forms.lecture.submit.questions.after"), widget=forms.CheckboxInput(attrs={'class': "form-check-input"}), required=False)
    minimal_lecture_length = forms.IntegerField(label=_("forms.lecture.submit.length.min"), widget=forms.NumberInput(attrs={'class': "form-control"}),)
    maximal_lecture_length = forms.IntegerField(label=_("forms.lecture.submit.length.max"), widget=forms.NumberInput(attrs={'class': "form-control"}),)
    additional_information_by_presentator = forms.CharField(label=_("forms.lecture.submit.info"), max_length=2048, widget=forms.Textarea(attrs={'class': "form-control"}),)
    related_website = forms.CharField(label=_("forms.lecture.submit.link"), max_length=100, widget=forms.URLInput(attrs={'class': "form-control"}), required=False)


# For edit and create:
class LectureForm(forms.Form):
    event = forms.ModelChoiceField(label=_("forms.lecture.event"), queryset=Event.objects.all(), widget=forms.Select(attrs={'class': "form-select"}))
    presentator = forms.ModelChoiceField(label=_("forms.lecture.moderator"), queryset=User.objects.all(), widget=forms.Select(attrs={'class': "form-select"}), required=False, blank=False)
    attendant = forms.ModelChoiceField(label=_("forms.lecture.attendant"), queryset=User.objects.filter(groups__name='Attendant'), widget=forms.Select(attrs={'class': "form-select"}), required=False, blank=False)
    title = forms.CharField(label=_("forms.lecture.title"), max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}),)
    description = forms.CharField(label=_("forms.lecture.description"), max_length=2048, widget=forms.Textarea(attrs={'class': "form-control"}),)
    target_group = forms.CharField(label=_("forms.lecture.group"), widget=forms.Select(choices=TARGET_GROUP, attrs={'class': "form-control"}))
    qualification_for_lecture = forms.CharField(label=_("forms.lecture.qualification"), max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}),)
    preferred_presentation_style = forms.CharField(label=_("forms.lecture.style"), widget=forms.Select(choices=PRESENTATION_STYLE, attrs={'class': "form-select"}))
    questions_during_lecture = forms.BooleanField(label=_("forms.lecture.questions.during"), widget=forms.CheckboxInput(attrs={'class': "form-check-input"}), required=False)
    questions_after_lecture = forms.BooleanField(label=_("forms.lecture.questions.after"), widget=forms.CheckboxInput(attrs={'class': "form-check-input"}), required=False)
    minimal_lecture_length = forms.IntegerField(label=_("forms.lecture.length.min"), widget=forms.NumberInput(attrs={'class': "form-control"}),)
    maximal_lecture_length = forms.IntegerField(label=_("forms.lecture.length.max"), widget=forms.NumberInput(attrs={'class': "form-control"}),)
    additional_information_by_presentator = forms.CharField(label=_("forms.lecture.moderator.info"), max_length=2048, widget=forms.Textarea(attrs={'class': "form-control"}), required=False)
    related_website = forms.CharField(label=_("forms.lecture.link"), max_length=100, widget=forms.URLInput(attrs={'class': "form-control"}), required=False)
    scheduled_in_room = forms.ModelChoiceField(label=_("forms.lecture.scheduled.room"), queryset=Room.objects.all(), widget=forms.Select(attrs={'class': "form-select"}), required=False)
    scheduled_presentation_time = forms.DateTimeField(label=_("forms.lecture.scheduled.datetime"), required=False, widget=forms.DateTimeInput(attrs={'class': "form-select"}))
    scheduled_presentation_length = forms.IntegerField(label=_("forms.lecture.scheduled.length"), widget=forms.NumberInput(attrs={'class': "form-control"}),)
    scheduled_presentation_style = forms.CharField(label=_("forms.lecture.scheduled.style"), widget=forms.Select(choices=PRESENTATION_STYLE, attrs={'class': "form-select"}), required=False)
    further_information = forms.CharField(label=_("forms.lecture.private.info"), max_length=2048, widget=forms.Textarea(attrs={'class': "form-control"}), required=False)
    link_to_material = forms.CharField(label=_("forms.lecture.link.material"), max_length=100, widget=forms.URLInput(attrs={'class': "form-control"}), required=False)
    link_to_recording = forms.CharField(label=_("forms.lecture.link.recording"), max_length=100, widget=forms.URLInput(attrs={'class': "form-control"}), required=False)
