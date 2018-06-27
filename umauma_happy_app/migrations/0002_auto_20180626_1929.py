# Generated by Django 2.0.6 on 2018-06-26 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('umauma_happy_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('factor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='umauma_happy_app.Factor')),
                ('history', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='umauma_happy_app.History')),
            ],
        ),
        migrations.RemoveField(
            model_name='data',
            name='past_achievement',
        ),
        migrations.AlterField(
            model_name='race',
            name='date',
            field=models.DateField(),
        ),
    ]
