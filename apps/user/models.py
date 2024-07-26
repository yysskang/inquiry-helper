from django.conf import settings
from django.db import models
from apps.base.base_model import Model


class UserAgreement(Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agreements')
    subscription_consent = models.BooleanField(default=False, verbose_name='구독 동의')
    marketing_consent = models.BooleanField(default=False, verbose_name='마케팅 동의')
    personal_info_consent = models.BooleanField(default=False, verbose_name='개인정보 동의')
