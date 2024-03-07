from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserChangeForm
from django.db import models

from django.contrib.auth.forms import UserChangeForm
from .models import Profile

from common.custom_widgets import PreviewImageFileWidget


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
        required=False,
        widget=forms.EmailInput(attrs={
            "placeholder" : "이메일",
        })
    )
    phone = forms.CharField(
        label="전화번호",
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
    
    address_choices = ((None, '선택'), ('서울', '서울'), ('인천', '인천'))
    address = forms.ChoiceField(
        label='주소',
        choices=address_choices,
    )
    
    description = forms.CharField(label="자기소개", required=False, widget=forms.Textarea())

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'nickname', 'phone', 'address', 'email', 'description']

class CustomUserChangeForm(UserChangeForm):
    password = None
    # UserChangeForm에서는 password를 수정할 수 없다.
    # 하지만 이렇게 None 값으로 지정해주지 않으면 password를 변경할 수 없다는 설명이 화면에 표현된다.
    class Meta:
        model = get_user_model()
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
        fields = ['nickname', 'phone', 'address', 'description','image',]
        labels = {
            'phone' : '전화번호',
            'address' : '주소'
        }