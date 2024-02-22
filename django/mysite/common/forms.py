from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserChangeForm
from django.db import models

from django.contrib.auth.forms import UserChangeForm
from .models import Profile

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

class CustomUserChangeForm(UserChangeForm):
    password = None
    # UserChangeForm에서는 password를 수정할 수 없다.
    # 하지만 이렇게 None 값으로 지정해주지 않으면 password를 변경할 수 없다는 설명이 화면에 표현된다.
    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name',]

        
class ProfileForm(forms.ModelForm):
    nickname = forms.CharField(label="별명", required=False)
    description = forms.CharField(label="자기소개", required=False, widget=forms.Textarea())
    image = forms.ImageField(label="이미지", required=False)
    # 위의 내용을 정의하지 않아도 상관없지만, 화면에 출력될 때 label이 영문으로 출력되는 것이 싫어서 수정한 것이다..
    class Meta:
        model = Profile
        fields = ['nickname', 'description', 'image',]