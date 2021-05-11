from django import forms
from captcha.fields import CaptchaField, CaptchaTextInput


class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=128, label='用户名',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username", 'autofocus': ''})
    )
    password = forms.CharField(
        max_length=256, label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"})
    )
    captcha = CaptchaField(label='验证码', widget=CaptchaTextInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.Form):

    username = forms.CharField(
        max_length=128, label='用户名',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        max_length=256, label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        max_length=256, label='确认密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码', widget=CaptchaTextInput(attrs={'class': 'form-control'}))
