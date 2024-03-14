from django.urls import path
from . import views
app_name = "recommandservice"


urlpatterns = [
    path('', views.index),
]