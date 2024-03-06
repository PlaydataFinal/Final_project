# kakaoapi/models.py
from django.db import models

class tour_kakao(models.Model):
    Name = models.CharField(max_length=255, db_column='Name')
    Address = models.CharField(max_length=255, db_column='Address')
    Latitude = models.FloatField(db_column='Latitude')
    Longitude = models.FloatField(db_column='Longitude')
    Image_URL = models.URLField(db_column='Image_URL')

    def __str__(self):
        return self.Name

    class Meta:
        # app_label을 'maria'로 설정하여 mariadb 데이터베이스에 모델을 매핑
        app_label = 'maria'
        db_table = 'tour_kakao'
