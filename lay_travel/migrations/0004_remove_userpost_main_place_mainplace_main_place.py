# Generated by Django 4.1.5 on 2023-01-20 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lay_travel', '0003_rename_main_place_name_mainplace_place_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpost',
            name='main_place',
        ),
        migrations.AddField(
            model_name='mainplace',
            name='main_place',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lay_travel.userpost'),
        ),
    ]
