from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model  # ユーザーモデルを取得するため


User = get_user_model()


class LoginForm(AuthenticationForm):
    # bootstrap4対応
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            # placeholderにフィールドのラベルを入れる
