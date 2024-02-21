from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserChangeForm
from django.db import models



class UserForm(UserCreationForm):
        # UserCreationForm을 상속받아 CustomUserCreationForm을 만든다.
    username = forms.CharField(
        label="아이디",
        widget=forms.TextInput(attrs={
            "placeholder": "아이디",
        })
    )
    password1 = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput(attrs={
            "placeholder": "비밀번호(8자 이상)",
        })
    )
    password2 = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput(attrs={
            "placeholder": "비밀번호 확인",
        })
    )
    email = forms.EmailField(
        label="이메일",
        widget=forms.EmailInput(attrs={
            "placeholder" : "이메일",
        })
    )
    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'email']
