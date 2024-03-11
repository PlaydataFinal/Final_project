from django.shortcuts import render
from rest_framework import generics
from .models import tour_kakao
from .serializers import TourKakaoSerializer
from rest_framework.pagination import PageNumberPagination
# Create your views here.
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'kakaoapi/kakao.html')# kakaoapi/views.py

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 15  # 한 페이지당 아이템 수
    page_size_query_param = 'page_size'
    max_page_size = 100

class TourKakaoList(generics.ListAPIView):
    serializer_class = TourKakaoSerializer
    pagination_class = CustomPageNumberPagination 
    def get_queryset(self):
        keyword = self.request.query_params.get('keyword', '')
        return tour_kakao.objects.filter(Name__icontains=keyword)



def image(request):
    # Get the first 10 tourist spots
    spots = tour_kakao.objects.all()[:10]
    return render(request, 'kakaoapi/kakao.html', {'spots': spots})