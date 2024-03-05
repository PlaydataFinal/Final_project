# ocr_app/urls.py

from django.urls import path
from . import views

app_name = 'ocr_app'

urlpatterns = [
    path('', views.index),
    path('process_image/', views.process_image, name='process_image'),
]