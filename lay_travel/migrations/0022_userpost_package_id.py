# Generated by Django 4.1.5 on 2023-05-23 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lay_travel', '0021_remove_package_main_place'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpost',
            name='package_id',
            field=models.IntegerField(null=True),
        ),
    ]
