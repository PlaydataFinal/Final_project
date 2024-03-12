from django.urls import path
from . import views
from .views import TourTmapList

urlpatterns = [
    path('', views.index),
    path('get_tourist_spots/', TourTmapList.as_view(), name='get_tourist_spots'),
]