# Generated by Django 5.0.6 on 2024-05-09 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("peru_api", "0002_category_rename_streams_tournament_channel_url"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="channel",
            name="url",
        ),
    ]
