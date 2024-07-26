from django.shortcuts import redirect
from django.urls import reverse


def is_login(func):

    def decorated(request, *args, **kwargs):

        if request.user.is_authenticated and not request.path in [reverse('user-login'), reverse('signup')]:
            return func(request, *args, **kwargs)
        else:
            return redirect('user-login')
    return decorated
