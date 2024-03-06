# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from test1.views import find_similar_places
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    # path('predict/', views.predict),
    path('find_similar_places/', find_similar_places, name='find_similar_places'),
]
