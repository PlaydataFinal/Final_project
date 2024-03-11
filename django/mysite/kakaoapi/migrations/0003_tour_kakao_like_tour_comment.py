# Generated by Django 4.1.13 on 2024-03-11 06:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kakaoapi', '0002_alter_tour_kakao_tel'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour_kakao',
            name='like',
            field=models.ManyToManyField(related_name='like_tour_kakao', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='tour_comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(db_column='Comment')),
                ('comment_like', models.IntegerField(db_column='Comment_Like', default=0)),
                ('create_date', models.DateTimeField()),
                ('modify_date', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kakaoapi.tour_kakao')),
            ],
        ),
    ]