# Generated by Django 2.0.5 on 2018-07-31 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('umauma_happy_app', '0005_auto_20180730_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='rank',
            field=models.IntegerField(null=True),
        ),
    ]
