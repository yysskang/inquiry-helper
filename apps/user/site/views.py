from django.shortcuts import redirect
from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = "index.html"


class Login(TemplateView):
    template_name = "user/login.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.session.get("contract_id"):
            return redirect('contract:contract-info')
        return super().dispatch(request, *args, **kwargs)


class Signup(TemplateView):
    template_name = "user/signup.html"
    def dispatch(self, request, *args, **kwargs):
        if self.request.session.get("contract_id"):
            return redirect('contract:contract-info')
        return super().dispatch(request, *args, **kwargs)


