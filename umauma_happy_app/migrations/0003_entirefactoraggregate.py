# Generated by Django 2.0.5 on 2018-07-04 01:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('umauma_happy_app', '0002_auto_20180626_1929'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntireFactorAggregate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('use', models.IntegerField()),
                ('hit', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('factor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='umauma_happy_app.Factor')),
            ],
        ),
    ]
