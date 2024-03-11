# ezocr/models.py
from django.db import models

class EzocrResult(models.Model):
    context = models.TextField(default="입력해주세요")
    question = models.TextField(default="이미지를 넣어주세요")
    answer = models.TextField(default="답변해주세요")
    image = models.ImageField(upload_to='ezocr_images/') 

    def __str__(self):
        return f"{self.question} - {self.answer}"