"""
ASGI config for making_sense_of_the_copyright_comments project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'making_sense_of_the_copyright_comments.settings')

application = get_asgi_application()
