# Generated by Django 4.1.5 on 2023-01-23 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lay_travel', '0014_remove_image_post_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='post_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lay_travel.postlocation'),
        ),
    ]
