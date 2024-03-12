# kakaoapi/models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class tour_kakao(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    Name = models.CharField(max_length=255, db_column='Name')
    Address = models.CharField(max_length=255, db_column='Address')
    Latitude = models.FloatField(db_column='Latitude')
    Longitude = models.FloatField(db_column='Longitude')
    Tel = models.CharField(max_length=255, db_column='Tel')  
    Image_URL = models.URLField(db_column='Image_URL')
    Tag = models.TextField(db_column='Tag')
    Hits = models.IntegerField(db_column='Hits', default=0)
    rec1 = 	models.IntegerField(db_column = 'rec1')
    rec2 =	models.IntegerField(db_column = 'rec2')
    rec3 = models.IntegerField(db_column = 'rec3')
    
    # 240311 추가내용
    like = models.ManyToManyField(User, related_name='like_tour_kakao')

    
    def __str__(self):
        return self.Name
    
# 240311 추가내용
class tour_comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_tour_comment')
    tour = models.ForeignKey(tour_kakao, on_delete=models.CASCADE)
    comment = models.TextField(db_column='Comment')
    comment_like = models.IntegerField(db_column='Comment_Like', default=0)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    like = models.ManyToManyField(User, related_name='like_tour_comment')
    
    def __str__(self):
        return self.author