# Generated by Django 5.0.6 on 2024-05-10 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("peru_api", "0004_remove_channel_channel_preview_channel_channel_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="channel",
            name="category",
            field=models.ManyToManyField(to="peru_api.category"),
        ),
    ]