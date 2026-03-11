"""
WSGI config for kurotsukisubs_firebase project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kurotsukisubs_firebase.settings')

application = get_wsgi_application()
