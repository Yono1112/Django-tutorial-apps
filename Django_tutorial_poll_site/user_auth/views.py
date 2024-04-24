from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, resolve_url

from .forms import LoginForm, SignupForm, UserUpdateForm


class TopView(generic.TemplateView):
    template_name = 'user_auth/top.html'


class Login(LoginView):
    form_class = LoginForm
    template_name = 'user_auth/login.html'


class Logout(LogoutView):
    template_name = 'user_auth/logout_done.html'


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        # 今ログインしてるユーザーのpkと、そのマイページのpkが同じなら許可
        user = self.request.user
        return user.pk == self.kwargs['pk']


class MyPage(OnlyYouMixin, generic.DetailView):
    model = User
    template_name = 'user_auth/my_page.html'


class Signup(generic.CreateView):
    template_name = 'user_auth/user_form.html'
    form_class = SignupForm

    def form_valid(self, form):
        form.save()
        # user = form.save()
        return redirect('user_auth:signup_done')

    # データ送信
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["process_name"] = "Sign up"
        return context


class SignupDone(generic.TemplateView):
    template_name = 'user_auth/signup_done.html'


class UserUpdate(OnlyYouMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user_auth/user_form.html'

    def get_success_url(self):
        return resolve_url('user_auth:my_page', pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["process_name"] = "Update"
        return context
