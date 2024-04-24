from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
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


class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'email','username', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = ''
            if field.label == '姓':
                field.widget.attrs['autofocus'] = ''
                field.widget.attrs['placeholder'] = 'Nakamoto'
            elif field.label == '名':
                field.widget.attrs['placeholder'] = 'Satoshi'
            elif field.label == 'メールアドレス':
                field.widget.attrs['placeholder'] = '***@proton.me'
