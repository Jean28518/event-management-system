from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

TARGET_GROUP = [
    ('BE', _('Beginner')),
    ('IN', _('Intermediate')),
    ('PR', _('Professional')),
]

PRESENTATION_STYLE = [
    ('RE', _('Recorded')),
    ('LI', _('Live')),
]


class Event(models.Model):
    name = models.CharField(max_length=100)   
    year = models.IntegerField()
    website = models.URLField()
    available_timeslots = models.CharField(max_length=2048, default="")
    call_for_papers = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name}"

    # TODO TimeSlots (nur Strings :)) 
    # TODO Tracks / Rooms


class Room(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField()
    coordinates = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.name}"


class Lecture(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    presentator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="presenting")
    attendant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attending", blank=True, null=True)
    title = models.CharField(max_length=100)   
    description = models.CharField(max_length=2048)   
    target_group = models.CharField(max_length=2, choices=TARGET_GROUP)
    available_timeslots = models.CharField(max_length=2048) # Encoded in JSON
    minimal_lecture_length = models.IntegerField() # (Minutes)
    maximal_lecture_length = models.IntegerField() # (Minutes)
    preferred_presentation_style = models.CharField(max_length=2, choices=PRESENTATION_STYLE)
    qualification_for_lecture = models.CharField(max_length=512)
    questions_during_lecture = models.BooleanField()
    questions_after_lecture = models.BooleanField()
    additional_information_by_presentator = models.CharField(max_length=2048) 
    scheduled_in_room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="held_in", blank=True, null=True)
    scheduled_presentation_time = models.DateTimeField(blank=True, null=True)
    scheduled_presentation_length = models.IntegerField(default=0) # (Minutes)
    scheduled_presentation_style = models.CharField(max_length=2, choices=PRESENTATION_STYLE)
    further_information = models.CharField(max_length=2048) 
    related_website = models.URLField()
    link_to_material = models.URLField()
    link_to_recording = models.URLField()

    def __str__(self):
        return f"{self.title}"
