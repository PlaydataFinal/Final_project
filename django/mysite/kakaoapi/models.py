# kakaoapi/models.py
from django.db import models

class tour_kakao(models.Model):        
    id = models.AutoField(primary_key=True, editable=False)  # id 필드 추가
    Name = models.CharField(max_length=255, db_column='Name')
    Address = models.CharField(max_length=255, db_column='Address')
    Latitude = models.FloatField(db_column='Latitude')
    Longitude = models.FloatField(db_column='Longitude')
    Tel = models.FloatField(db_column = 'Tel')
    Image_URL = models.URLField(db_column='Image_URL')


    def __str__(self):
        return self.Name


