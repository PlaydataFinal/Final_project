#tmapapi/views.py
from django.shortcuts import render
from rest_framework import generics
from .models import tour_tmap
from .serializers import TourTmapSerializer

from django.http import HttpResponse
from rest_framework.response import Response
from django.db.models import Q


def index(request):
    return render(request, 'tmapapi/tmap.html')

class TourTmapList(generics.ListAPIView):
    serializer_class = TourTmapSerializer

    def get_queryset(self):
        departure = self.request.query_params.get('departure', '')
        destination = self.request.query_params.get('destination', '')
        print(f"keyword --> {departure}")
        print(f"keyword --> {destination}")
        print(f"keyword --> {self.request}")
        queryset = tour_tmap.objects.all()

        if departure or destination:
            queryset = queryset.filter(Q(Name__iexact=departure) | Q(Name__iexact=destination))
            print(queryset)

        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)