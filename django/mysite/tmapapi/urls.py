#tmapapi/urls.py
from django.urls import path
from . import views
from .views import TourTmapList

app_name = "tmapapi"


urlpatterns = [
    path('', views.index, name='index'),
    path('get_tourist_spots/', TourTmapList.as_view(), name='get_tourist_spots'),
]