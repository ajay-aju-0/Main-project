# Generated by Django 3.2.4 on 2023-03-21 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20230320_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='profile',
            field=models.ImageField(default='null', max_length=300, upload_to='DP', verbose_name='profile photo'),
        ),
    ]
