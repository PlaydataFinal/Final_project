# models.py
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # User모델과 Profile을 1:1로 연결
    description = models.TextField(blank=True)
    nickname = models.CharField(max_length=40, blank=True, null=True)
    image = models.ImageField(blank=True)
    
    phoneNumberRegex = RegexValidator(regex = r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
    phone = models.CharField(validators = [phoneNumberRegex], max_length = 11, unique = True)
    
    email = models.EmailField(max_length=150, blank=True, null=True)
    
    address_choices = ((None, '선택'), ('서울', '서울'), ('인천', '인천'))
    address = models.CharField(max_length=50, choices=address_choices, verbose_name='주소',)

    is_first = models.BooleanField(default = True)

    # class Meta:
    #     app_label = "maria"
    #     db_table = 'Profile'
