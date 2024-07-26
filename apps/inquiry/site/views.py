from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from apps.contract.models import Contract
from apps.inquiry.models import InquiryManagement as InquiryManagementModel, Inquiry
from config.decorators import is_login


@method_decorator(is_login, name='dispatch')
class InquiryList(TemplateView):
    template_name = "inquiry/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        return context


@method_decorator(is_login, name='dispatch')
class InquiryDetail(TemplateView):
    template_name = "inquiry/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        return context


@method_decorator(is_login, name='dispatch')
class InquiryManagement(TemplateView):
    template_name = "inquiry/management.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        return context

class InquiryService(TemplateView):
    template_name = "inquiry/service.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        api_key = kwargs.get('key')

        contract = get_object_or_404(Contract, api_key=api_key)
        inquiry_management = get_object_or_404(InquiryManagementModel, contract=contract)

        inquiry_data = {
            'name': inquiry_management.name,
            'phone': inquiry_management.phone,
            'email': inquiry_management.email,
            'attachment': inquiry_management.attachment,
            'link': inquiry_management.link,
            'date_time': inquiry_management.date_time,
            'time_placeholder': inquiry_management.time_placeholder,
            'address': inquiry_management.address,
            'inquiry_types': [{'id': it.id, 'name': it.name} for it in inquiry_management.inquiry_types.all()]
        }

        context['inquiry'] = inquiry_data
        return context