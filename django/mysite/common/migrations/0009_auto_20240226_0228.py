# Generated by Django 3.1.1 on 2024-02-26 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0008_auto_20240226_0206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, choices=[(None, '선택'), ('서울', '서울'), ('인천', '인천')], max_length=50, null=True, verbose_name='주소'),
        ),
    ]
