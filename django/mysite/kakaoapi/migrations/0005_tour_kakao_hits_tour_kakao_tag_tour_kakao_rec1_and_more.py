# Generated by Django 4.1.13 on 2024-03-12 11:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kakaoapi', '0004_merge_20240312_0926'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='tour_kakao',
        #     name='Hits',
        #     field=models.IntegerField(db_column='Hits', default=0),
        # ),
        # migrations.AddField(
        #     model_name='tour_kakao',
        #     name='Tag',
        #     field=models.TextField(db_column='Tag', default=''),
        # ),
        # migrations.AddField(
        #     model_name='tour_kakao',
        #     name='rec1',
        #     field=models.IntegerField(db_column='rec1', default=0),
        # ),
        # migrations.AddField(
        #     model_name='tour_kakao',
        #     name='rec2',
        #     field=models.IntegerField(db_column='rec2', default=0),
        # ),
        # migrations.AddField(
        #     model_name='tour_kakao',
        #     name='rec3',
        #     field=models.IntegerField(db_column='rec3', default=0),
        # ),
        # migrations.AlterField(
        #     model_name='tour_comment',
        #     name='author',
        #     field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_tour_comment', to=settings.AUTH_USER_MODEL),
        # ),
        # migrations.AlterField(
        #     model_name='tour_comment',
        #     name='comment_like',
        #     field=models.ManyToManyField(related_name='like_tour_comment', to=settings.AUTH_USER_MODEL),
        # ),
    ]