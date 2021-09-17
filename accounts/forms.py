from allauth.account.forms import LoginForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User

from accounts.models import Profile
from utils.forms import update_fields_widget


class CleanMixin:

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if full_name:
            full_name = full_name.split()
            if len(full_name) != 2:
                raise forms.ValidationError(f'Введите 2 слова, имя и фамилию через пробел')
        return full_name

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Пользователь с email: {email} уже существует')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователь с никнеймом: {username} уже существует')
        return cleaned_data


class CustomUserCreationForm(CleanMixin, UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_fields_widget(self, ('email', 'username', 'password1', 'password2',
                                    'first_name', 'last_name'), 'form-control')


class ProfileUpdateForm(CleanMixin, forms.ModelForm):
    email = forms.EmailField(label='Адресс электронной почты', required=False)
    username = forms.CharField(max_length=150, label='Имя пользователя', required=False)
    full_name = forms.CharField(max_length=150, label='Имя и фамилия', required=False)

    class Meta:
        model = Profile
        fields = ('avatar', 'email', 'username', 'full_name', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_fields_widget(self, ('avatar', 'email', 'username', 'full_name',), 'form-control')


class CustomAuthenticationForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_fields_widget(self, ('login', 'password'), 'form-control')


class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_fields_widget(self, ('old_password', 'new_password1', 'new_password2'), 'form-control')


class CustomPasswordResetForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_fields_widget(self, ('email',), 'form-control')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Пользователя с email: {email} не существует')
        return cleaned_data


class CustomSetPasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_fields_widget(self, ('new_password1', 'new_password2',), 'form-control')
