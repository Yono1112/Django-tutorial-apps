from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User


from .forms import LoginForm


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
    # モデル名小文字(user)でモデルインスタンスがテンプレートファイルに渡される
