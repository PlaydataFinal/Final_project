from django.urls import path
from . import views
from .views import TourKakaoList

app_name = "kakaoapi"

urlpatterns = [
    path('', views.index, name='index'),
    path('get_tourist_spots/', TourKakaoList.as_view(), name='get_tourist_spots'),
]