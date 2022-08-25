"""
ASGI config for event_management_system project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from . import set_rights

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management_system.settings')
set_rights.init()
application = get_asgi_application()
