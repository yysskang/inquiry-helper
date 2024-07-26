from django.urls import path
from api.v1.health import health_check


urlpatterns = [
    path('health/', health_check, name='health_check'),
]
