from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.models import Group, Permission

organisator_permissions = [
        "add_lecture",
        "change_lecture",
        "delete_lecture",
        "view_lecture",
        "add_room",
        "change_room",
        "delete_room",
        "view_room",
        "add_email",
        "change_email",
        "delete_email",
        "view_email",
        "add_event",
        "change_event",
        "delete_event",
        "view_event",
        "add_profile",
        "change_profile",
        "delete_profile",
        "view_profile",
        ]

attendant_permissions = [
        "view_lecture",
        "view_event",
        "view_profile",
        "add_lecture",
        "change_lecture",
        "change_profile",
        ]

contact_permissions = [
        "add_lecture",
        ]



def init():
    admin_group, created = Group.objects.get_or_create(name='Administrator')
    organisator_group, created = Group.objects.get_or_create(name='Organisator')
    attendant_group, created = Group.objects.get_or_create(name='Attendant')
    contact_group, created = Group.objects.get_or_create(name='Contact')
    
    admin_group.permissions.clear()
    organisator_group.permissions.clear()
    attendant_group.permissions.clear()
    contact_group.permissions.clear()


    for permission in get_all_permissions():
        admin_group.permissions.add(Permission.objects.get(codename=permission.split(".")[1]))

    for permission in organisator_permissions:
        organisator_group.permissions.add(Permission.objects.get(codename=permission))

    for permission in attendant_permissions:
        attendant_group.permissions.add(Permission.objects.get(codename=permission))

    for permission in contact_permissions:
        contact_group.permissions.add(Permission.objects.get(codename=permission))

def get_all_permissions():
    permissions = []

    tmp_superuser = get_user_model()(is_active=True, is_superuser=True)

    for backend in auth.get_backends():
        if hasattr(backend, "get_all_permissions"):
            for permission in backend.get_all_permissions(tmp_superuser):
                permissions.append(permission)

    sorted_list_of_permissions = sorted(list(permissions))
    
    # for permission in sorted_list_of_permissions:
    #     print(permission)

    return sorted_list_of_permissions