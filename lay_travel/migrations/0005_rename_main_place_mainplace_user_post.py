# Generated by Django 4.1.5 on 2023-01-20 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lay_travel', '0004_remove_userpost_main_place_mainplace_main_place'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mainplace',
            old_name='main_place',
            new_name='user_post',
        ),
    ]
