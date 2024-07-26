from django.db import models
from django.db.models import Q


class InquiryManagementQuerySet(models.QuerySet):
    def with_inquiry_types(self):
        return self.prefetch_related('inquiry_types')

    def active_inquiries(self):
        return self.filter(
            Q(name=True) | Q(phone=True) | Q(email=True) | Q(attachment=True) | Q(link=True) | Q(date_time=True)
        ).select_related('contract')