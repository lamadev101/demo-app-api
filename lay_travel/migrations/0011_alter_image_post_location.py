# Generated by Django 4.1.5 on 2023-01-23 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lay_travel', '0010_remove_image_main_place_image_post_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='post_location',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='lay_travel.postlocation'),
        ),
    ]
