from users.models import Profile
from django.contrib.auth.models import User
from events.models import Event, Lecture, Room

class meta:

    def get_all_fields():
        return_value = []
        for string in meta.get_fields_user():
            return_value.append(string)
        for string in meta.get_fields_lecture():
            return_value.append(string)
        for string in meta.get_fields_attendant():
            return_value.append(string)
        for string in meta.get_fields_event():
            return_value.append(string)
        for string in meta.get_fields_room():
            return_value.append(string)
        return return_value


    def get_fields_user():
        return_value = []
        for field in User._meta.fields:
            return_value.append(f"$user.{field.attname}")
        for field in Profile._meta.fields:
            return_value.append(f"$user.profile.{field.attname}")
            
        return return_value


    def get_fields_lecture():
        return_value = []
        for field in Lecture._meta.fields:
            return_value.append(f"$lecture.{field.attname}")
        return return_value


    def get_fields_attendant():
        return_value = []
        for field in User._meta.fields:
            return_value.append(f"$attendant.{field.attname}")
        for field in Profile._meta.fields:
            return_value.append(f"$attendant.profile.{field.attname}")
        return return_value


    def get_fields_room():
        return_value = []
        for field in Room._meta.fields:
            return_value.append(f"$room.{field.attname}")
        return return_value


    def get_fields_event():
        return_value = []
        for field in Event._meta.fields:
            return_value.append(f"$event.{field.attname}")
        return return_value