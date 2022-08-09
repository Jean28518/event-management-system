from django.contrib import admin

from .models import Event, Room, Lecture

# Register your models here.
admin.site.register(Event)
admin.site.register(Room)
admin.site.register(Lecture)
