# Generated by Django 3.2.4 on 2023-05-16 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0030_auto_20230505_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffs',
            name='salary',
            field=models.BigIntegerField(verbose_name='Basic pay'),
        ),
    ]