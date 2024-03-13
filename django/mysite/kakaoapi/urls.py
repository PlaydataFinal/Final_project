from django.urls import path
from . import views
from .views import TourKakaoList

app_name = "kakaoapi"

urlpatterns = [
    path('', views.index, name='index'),
    path('get_tourist_spots/', TourKakaoList.as_view(), name='get_tourist_spots'),
    path('tour/<int:tour_id>/', views.tour_detail, name='tour_detail'),
    path('comment_create/<int:tour_id>/', views.comment_create, name='comment_create'),
    path('comment/modify/<int:comment_id>/', views.comment_modify, name='comment_modify'),
    path('comment/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    path('tour/like/<int:tour_id>/', views.tour_like, name='tour_like'),
    path('comment/like/<int:comment_id>/', views.comment_like, name='comment_like'),

]