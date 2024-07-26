from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from apps.contract.models import Contract
from config.decorators import is_login


@method_decorator(is_login, name='dispatch')
class ContractInfo(TemplateView):
    template_name = "contract/info.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        contract_id = self.request.session.get('contract_id', None)
        if not Contract.objects.filter(id=contract_id).exists():
            self.template_name = "contract/write.html"
        else:
            contract = Contract.objects.get(id=contract_id)
            context['contract'] = contract
        return context
