"""
WSGI config for event_management_system project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from . import set_rights

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management_system.settings')
set_rights.init()
application = get_wsgi_application()
