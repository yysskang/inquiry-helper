from django.urls import path
from apps.user.site.views import Login, Signup, Index

app_name = ""

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path("login/", Login.as_view(), name="user-login"),
    path("signup/", Signup.as_view(), name="signup"),
]