# Generated by Django 4.1.13 on 2024-03-06 06:51

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('nickname', models.CharField(blank=True, max_length=40, null=True)),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('phone', models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator(regex='^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')])),
                ('email', models.EmailField(blank=True, max_length=150, null=True)),
                ('address', models.CharField(choices=[(None, '선택'), ('서울', '서울'), ('인천', '인천')], max_length=50, verbose_name='주소')),
                ('is_first', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]