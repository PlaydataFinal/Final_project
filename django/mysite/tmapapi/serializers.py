# tmapapi/serializers.py
from dataclasses import field
from rest_framework import serializers
from .models import tour_tmap

class TourTmapSerializer(serializers.ModelSerializer):
    class Meta:
        model = tour_tmap
        fields = '__all__'
