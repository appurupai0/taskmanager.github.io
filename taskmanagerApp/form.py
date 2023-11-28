import hashlib

from django import forms
from .models import Users


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="メールアドレス",
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'メールアドレス', 'class': 'form-control'}
        )
    )
    password = forms.CharField(
        label="パスワード",
        required=False,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'パスワード', 'class': 'form-control'}
        )
    )

    # バリデーション処理
    # email and password validation（複数項目を指定するvalidation -> clean(self)という記述をする
    def clean(self):
        # super().clean()で親のcleanを呼び出す（必須
        cleaned_data = super().clean()
        # emailタグに入力されている値を取得
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        # passwordをハッシュ値に変換
        hs_password = hashlib.md5(password.encode()).hexdigest()
        # いずれかの入力値無し
        if not email or not password:
            raise forms.ValidationError("メールアドレス、パスワードを入力してください")
        # 登録データと一致かどうか
        if not Users.objects.filter(email=email, password=hs_password).exists():
            raise forms.ValidationError("メールアドレスとパスワードが一致しません")
        # 複数のデータを返すself.cleaned_data (email,passwordを返す)
        return self.cleaned_data


# register画面form
class UserResisterForm(forms.Form):
    name = forms.CharField(
        label="ユーザー名",
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'ユーザー名', 'class': 'form-control mb-1'}
        )
    )
    email = forms.EmailField(
        label="メールアドレス",
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'メールアドレス', 'class': 'form-control mb-1'}
        )
    )
    password = forms.CharField(
        label="パスワード",
        required=False,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'パスワード', 'class': 'form-control mb-1'}
        )
    )
    conf_password = forms.CharField(
        label="確認パスワード",
        required=False,
        widget=forms.PasswordInput(
            attrs={'placeholder': '確認パスワード', 'class': 'form-control mb-1'}
        )
    )

    # register validation　複数field参照
    def clean(self):
        # super().clean()で親のcleanを呼び出す（必須
        cleaned_data = super().clean()
        # new_email 入力値の取得
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        conf_password = cleaned_data.get('conf_password')
        # 入力されているか
        if not name or not email or not password or not conf_password:
            raise forms.ValidationError("すべての項目を記入してください")
        # user_name登録されているか
        if Users.objects.filter(user_name=name).exists():
            raise forms.ValidationError("このユーザー名は既に登録されています")
        # 既に登録されているか
        if Users.objects.filter(email=email).exists():

            raise forms.ValidationError("このメールアドレスは既に登録されています")
        # passwordが一致しているか
        if password != conf_password:
            raise forms.ValidationError("パスワードが一致していません")
        # 大文字小文字が１文字以上含まれているか
        if password.islower() or password.isupper() or password.isdecimal():
            # errorメッセージを格納
            # template側で表示
            self.add_error(None, "パスワードは大文字と小文字を１文字以上含んで入力してください")
        # 8文字以上13文字未満で入力されているか
        if not 8 <= len(password) < 13:
            # errorメッセージを格納
            self.add_error(None, "パスワードは８文字以上１３文字未満で入力してください")
        # validation　OKで戻り値
        # 複数のデータを返すself.cleaned_data (email,password,conf_passwordを返す)
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        initial_values = kwargs.pop('initial_values', {})
        super(UserResisterForm, self).__init__(*args, **kwargs)

        # セッション情報があればそれを初期値にセット
        self.fields['name'].initial = initial_values.get('user_name', '')
        self.fields['email'].initial = initial_values.get('email', '')
        self.fields['password'].initial = initial_values.get('password', '')
