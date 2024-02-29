from django.urls import path 
from django.contrib.auth import views as auth_views
from . import views
app_name = "common"

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="common/login.html") , name="login"),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name="profile"),
    path('<str:username>/', views.people, name="people"),
    path('/first/', views.first, name='first'),

]

