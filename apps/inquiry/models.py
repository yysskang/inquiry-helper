from django.db import models
from apps.base.base_model import Model
from apps.contract.models import Contract
from apps.inquiry.manager import InquiryManagementQuerySet
from util.aes256 import AES256


class Inquiry(Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='inquiries')
    name = models.CharField(verbose_name="이름", max_length=100, null=True, blank=True)
    phone = models.CharField(verbose_name="폰번호", max_length=20, null=True, blank=True)
    email = models.EmailField(verbose_name="이메일", null=True, blank=True)
    title = models.CharField(verbose_name="문의 제목", max_length=200)
    content = models.TextField(verbose_name="문의 내용")
    file = models.URLField(verbose_name="파일 링크", null=True, blank=True)
    type = models.CharField(verbose_name="문의 타입", max_length=100, null=True, blank=True)
    link = models.URLField(verbose_name="링크", null=True, blank=True)
    date_time = models.DateTimeField(verbose_name="시간", null=True, blank=True)
    address = models.CharField(verbose_name="주소", max_length=255, null=True, blank=True)
    param1 = models.CharField(verbose_name="파라미터1", max_length=255, null=True, blank=True)
    param2 = models.CharField(verbose_name="파라미터2", max_length=255, null=True, blank=True)
    param3 = models.CharField(verbose_name="파라미터3", max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        aes256 = AES256()
        if self.name:
            self.name = aes256.encrypt_ase(self.name)
        if self.phone:
            self.phone = aes256.encrypt_ase(self.phone)
        if self.email:
            self.email = aes256.encrypt_ase(self.email)
        if self.address:
            self.address = aes256.encrypt_ase(self.address)
        super().save(*args, **kwargs)


class InquiryType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class InquiryManagement(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='inquiry_management')
    name = models.BooleanField(default=True)
    phone = models.BooleanField(default=True)
    email = models.BooleanField(default=True)
    attachment = models.BooleanField(default=True)
    link = models.BooleanField(default=True)
    date_time = models.BooleanField(default=True)
    time_placeholder = models.CharField(max_length=255, null=True, blank=True)
    address = models.BooleanField(default=True)
    inquiry_types = models.ManyToManyField(InquiryType, related_name='inquiry_managements')

    objects = InquiryManagementQuerySet.as_manager()
