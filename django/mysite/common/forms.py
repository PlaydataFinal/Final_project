from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserChangeForm
from django.db import models

from django.contrib.auth.forms import UserChangeForm
from .models import Profile

from common.custom_widgets import PreviewImageFileWidget
from django.core.validators import RegexValidator


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
    first_name = forms.CharField(
        label="성",
        widget=forms.TextInput(attrs={
            "placeholder": "성",
        })
    )
    last_name = forms.CharField(
        label="이름",
        widget=forms.TextInput(attrs={
            "placeholder": "이름",
        })
    )
    email = forms.EmailField(
        label="이메일",
        required=False,
        widget=forms.EmailInput(attrs={
            "placeholder" : "이메일",
        })
    )
    phoneNumberRegex = RegexValidator(regex = r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$', message='숫자만 입력해주세요.')
    phone = forms.CharField(
        label="전화번호",
        validators=[phoneNumberRegex],
        max_length=11,
        widget=forms.TextInput(attrs={
            "placeholder" : "전화번호",
        })
    )
    nickname = forms.CharField(
        label="닉네임",
        widget=forms.TextInput(attrs={
            "placeholder" : "닉네임",
        })
    )
    image = forms.ImageField(
        label="프로필사진",
        required=False,
        widget=PreviewImageFileWidget,
    )
    
    description = forms.CharField(label="자기소개", required=False, widget=forms.Textarea())

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'nickname', 'phone', 'email', 'description']
        labels = {
            'first_name' : '성',
            'last_name' : '이름'
        }
        

class CustomUserChangeForm(UserChangeForm):
    password = None
    # UserChangeForm에서는 password를 수정할 수 없다.
    # 하지만 이렇게 None 값으로 지정해주지 않으면 password를 변경할 수 없다는 설명이 화면에 표현된다.
    class Meta:
        model = get_user_model()
        app_label = 'default'
        fields = ['first_name', 'last_name','email', ]
        labels = {
            'email' : '이메일',
            'first_name' : '성',
            'last_name' : '이름'
        }

        
class ProfileForm(forms.ModelForm):
    nickname = forms.CharField(label="닉네임", required=False)
    description = forms.CharField(label="자기소개", required=False, widget=forms.Textarea())
    image = forms.ImageField(label="프로필사진", required=False, widget=PreviewImageFileWidget,)
    # 위의 내용을 정의하지 않아도 상관없지만, 화면에 출력될 때 label이 영문으로 출력되는 것이 싫어서 수정한 것이다..
    class Meta:
        model = Profile
        app_label = 'default',
        fields = ['nickname', 'phone', 'description','image',]
        labels = {
            'phone' : '전화번호',
        }