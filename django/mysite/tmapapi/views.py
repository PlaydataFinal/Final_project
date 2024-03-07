from django.shortcuts import render
from rest_framework import generics
from .models import tour_kakao
from .serializers import TourKakaoSerializer
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'tmapapi/tmap.html')


class TourKakaoList(generics.ListAPIView):
    serializer_class = TourKakaoSerializer

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword', '')
        return tour_kakao.objects.filter(Name__icontains=keyword)