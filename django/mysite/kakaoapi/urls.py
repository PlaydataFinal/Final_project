from django.urls import path
from . import views
from .views import TourKakaoList
urlpatterns = [
    path('', views.index),
    path('get_tourist_spots/', TourKakaoList.as_view(), name='get_tourist_spots'),
]