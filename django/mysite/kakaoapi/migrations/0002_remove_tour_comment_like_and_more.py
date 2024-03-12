# Generated by Django 4.1.13 on 2024-03-12 09:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kakaoapi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tour_comment',
            name='comment_like',
        ),
        migrations.AddField(
            model_name='tour_comment',
            name='comment_like',
            field=models.ManyToManyField(default=0, related_name='like_tour_comment', to=settings.AUTH_USER_MODEL),
        ),
    ]
