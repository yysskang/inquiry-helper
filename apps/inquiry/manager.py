from django.db import models
from django.db.models import Q
from django.db.models import Count, Case, When, IntegerField


class InquiryManagementQuerySet(models.QuerySet):
    def with_inquiry_types(self):
        return self.prefetch_related('inquiry_types')

    def active_inquiries(self):
        return self.filter(
            Q(name=True) | Q(phone=True) | Q(email=True) | Q(attachment=True) | Q(link=True) | Q(date_time=True)
        ).select_related('contract')


class InquiryQuerySet(models.QuerySet):

    def with_contract(self, contract_id, inquiry_id):
        return self.filter(contract=contract_id, id=inquiry_id)

    def with_counts(self, contract_id):
        return self.filter(contract=contract_id).aggregate(
            total_count=Count('id'),
            status_false_count=Count(Case(When(status=False, then=1), output_field=IntegerField()))
        )
