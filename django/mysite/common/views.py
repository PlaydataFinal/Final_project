# common/views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from .forms import UserForm

from django.contrib.auth import logout
from django.shortcuts import redirect

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from django.contrib.auth.models import User

from .models import Profile

from .forms import CustomUserChangeForm, ProfileForm


from django.contrib.auth.forms import UserCreationForm
# Django 프레임워크가 구현해 놓은 회원가입 폼을 import 한다.

# def signup(request):
#     """
#     계정생성
#     """
#     if request.method == "POST":
#         form = UserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             print(form)
#             print('-'*50)
#             print('phone : ' + form.cleaned_data.get('phone'))
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('index')
#     else:
#         form = UserForm()
#     return render(request, 'common/signup.html', {'form': form})
# views.py

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password1"])
            nickname = request.POST["nickname"]
            email = request.POST["email"]
            phone = request.POST["phone"]
            profile = Profile(user=user, nickname=nickname, phone=phone, email=email)
            profile.save()
            login(request,user)
            return redirect('main')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})
    
def logout_view(request):
    logout(request)
    return redirect('index')

def people(request, username): # urls.py에서 넘겨준 인자를 username으로 받는다.
    person = get_object_or_404(get_user_model(), username=username)
    return render(request, 'common/people.html', {'person': person})

def profile(request):
    if request.method == 'POST':
        user_change_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_change_form.is_valid() and profile_form.is_valid():
            user = user_change_form.save()
            profile_form.save()
            return redirect('common:people', user.username)
        return redirect('common:profile')
    else:
        user_change_form = CustomUserChangeForm(instance=request.user)
        # 새롭게 추가하는 것이 아니라 수정하는 것이기 때문에
        # 기존의 정보를 가져오기 위해 instance를 지정해야 한다.
        profile, create = Profile.objects.get_or_create(user=request.user)
        # Profile 모델은 User 모델과 1:1 매칭이 되어있지만
        # User 모델에 새로운 인스턴스가 생성된다고 해서 그에 매칭되는 Profile 인스턴스가 생성되는 것은 아니기 때문에
        # 매칭되는 Profile 인스턴스가 있다면 그것을 가져오고, 아니면 새로 생성하도록 한다.
        profile_form = ProfileForm(instance=profile)
        return render(request, 'common/profile.html', {
            'user_change_form': user_change_form,
            'profile_form': profile_form
        })
        
def first(request):
    # user = get_object_or_404(get_user_model(), username=username)
    # print(f'request : {request}')
    # profile = get_object_or_404(Profile, user=request.user)
    profile = Profile.objects.get(user=request.user)
    profile.is_first = False
    profile.save()
    return render(request, 'common/first.html')