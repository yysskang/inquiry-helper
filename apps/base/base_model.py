from django.db import models


class Model(models.Model):
    """Base override class for `django.db.models.Model`."""

    created = models.DateField(verbose_name="생성일자", auto_now_add=True)
    created_at = models.DateTimeField(verbose_name="생성일시", auto_now_add=True)
    modified = models.DateField(verbose_name="수정일자", auto_now=True)
    modified_at = models.DateTimeField(verbose_name="수정일시", auto_now=True)
    remark = models.TextField(verbose_name="비고", blank=True, null=True)

    class Meta:
        abstract = True
