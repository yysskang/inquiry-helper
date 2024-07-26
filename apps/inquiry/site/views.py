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
        contract_id = self.request.session.get("contract_id")
        if contract_id:
            inquiry_counts = Inquiry.objects.with_counts(contract_id)
            context['inquiry_count'] = inquiry_counts.get("total_count")
            context['status_false_count'] = inquiry_counts.get('status_false_count')
            context['contract'] = (Contract.objects.filter(id=contract_id).
                                   values('company_name', 'expiration_date').first())
        return context


@method_decorator(is_login, name='dispatch')
class InquiryDetail(TemplateView):
    template_name = "inquiry/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        inquiry_id = kwargs.get('pk')
        contract_id = self.request.session.get("contract_id")
        Inquiry.objects.with_contract(contract_id, inquiry_id).update(status=True)
        inquiry = get_object_or_404(Inquiry, pk=inquiry_id)
        context['inquiry'] = inquiry

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
        inquiry_management = InquiryManagementModel.objects.filter(contract=contract).first()

        if inquiry_management:
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
            context['company_name'] = contract.company_name
        else:
            context['message'] = '[문의 관리] 메뉴를 통해 설정이 필요합니다.'
        return context