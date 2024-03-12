# tmapapi/models.py
from django.db import models
from django.conf import settings

class tour_tmap(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    Name = models.CharField(max_length=255, db_column='Name')
    Address = models.CharField(max_length=255, db_column='Address')
    Latitude = models.FloatField(db_column='Latitude')
    Longitude = models.FloatField(db_column='Longitude')
    Tel = models.CharField(max_length=255, db_column='Tel')  
    Image_URL = models.URLField(db_column='Image_URL')

    def __str__(self):
        return self.Name