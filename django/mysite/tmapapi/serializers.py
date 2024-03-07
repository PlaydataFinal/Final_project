# tmapapi/serializers.py

from rest_framework import serializers
from .models import tour_kakao

class TourKakaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = tour_kakao
        fields = '__all__'
