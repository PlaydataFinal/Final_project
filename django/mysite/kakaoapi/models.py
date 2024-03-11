# kakaoapi/models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class tour_kakao(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    Name = models.CharField(max_length=255, db_column='Name')
    Address = models.CharField(max_length=255, db_column='Address')
    Latitude = models.FloatField(db_column='Latitude')
    Longitude = models.FloatField(db_column='Longitude')
    Tel = models.CharField(max_length=255, db_column='Tel')  
    Image_URL = models.URLField(db_column='Image_URL')
    
    # 240311 추가내용
    like = models.ManyToManyField(User, related_name='like_tour_kakao')

    
    def __str__(self):
        return self.Name
    
# 240311 추가내용
class tour_comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(tour_kakao, on_delete=models.CASCADE)
    comment = models.TextField(db_column='Comment')
    comment_like = models.IntegerField(db_column='Comment_Like', default=0)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

    
    def __str__(self):
        return self.Name