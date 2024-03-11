from django.urls import path
from .views import ezocr

app_name = 'ezocr'
urlpatterns = [
    path('', ezocr, name='ezocr'),
]