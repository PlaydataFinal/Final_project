#ocr/urls.py
from django.urls import path
from . import views

app_name = 'ocr' 

urlpatterns = [
    path('', views.index, name='ocr'),
    path('predict/', views.predict, name='predict'),
]