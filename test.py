import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from django.contrib.auth.models import User

from apps.inquiry.models import Inquiry

print(Inquiry.objects.values().all())
