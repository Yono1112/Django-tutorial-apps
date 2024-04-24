from django.views import generic
from django.contrib.auth.views import LoginView

from .forms import LoginForm


class TopView(generic.TemplateView):
    template_name = 'user_auth/top.html'


class Login(LoginView):
    form_class = LoginForm
    template_name = 'user_auth/login.html'
