# Generated by Django 3.2.4 on 2023-03-17 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20230315_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animals',
            name='status',
            field=models.IntegerField(),
        ),
    ]
