import os
from django.core.wsgi import get_wsgi_application

# Ensure the config.settings module is used by WSGI
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
