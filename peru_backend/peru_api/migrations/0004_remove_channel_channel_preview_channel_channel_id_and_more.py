# Generated by Django 5.0.6 on 2024-05-09 09:57

import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("peru_api", "0003_remove_channel_url"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="channel",
            name="channel_preview",
        ),
        migrations.AddField(
            model_name="channel",
            name="channel_id",
            field=models.CharField(default="", max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="channel",
            name="country",
            field=django_countries.fields.CountryField(
                default="", max_length=2, null=True
            ),
        ),
        migrations.AddField(
            model_name="channel",
            name="lang",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="channel",
            name="logo",
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name="channel",
            name="owners",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="channel",
            name="website",
            field=models.URLField(null=True),
        ),
    ]