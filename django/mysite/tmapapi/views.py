from django.shortcuts import render
from rest_framework import generics
from .models import tour_tmap
from .serializers import TourTmapSerializer

# Create your views here.
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'tmapapi/tmap.html')


class TourTmapList(generics.ListAPIView):
    serializer_class = TourTmapSerializer

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword', '')
        return tour_tmap.objects.filter(Name__icontains=keyword)