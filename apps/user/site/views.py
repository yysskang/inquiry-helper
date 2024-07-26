from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = "index.html"


class Login(TemplateView):
    template_name = "user/login.html"


class Signup(TemplateView):
    template_name = "user/signup.html"

