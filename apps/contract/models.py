from django.conf import settings
from django.db import models
from apps.base.base_model import Model


class Contract(Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contract')
    company_name = models.CharField(max_length=255)
    website_url = models.URLField()
    api_key = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True, help_text='활성화 기간')
    expiration_date = models.DateField(verbose_name="계약 만료일")
