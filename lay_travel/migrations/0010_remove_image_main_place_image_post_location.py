# Generated by Django 4.1.5 on 2023-01-23 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lay_travel', '0009_rename_main_place_userpost_main_place_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='main_place',
        ),
        migrations.AddField(
            model_name='image',
            name='post_location',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='lay_travel.postlocation'),
        ),
    ]
