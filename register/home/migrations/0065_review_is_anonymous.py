# Generated by Django 3.0 on 2020-11-14 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0064_auto_20201018_1453"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="is_anonymous",
            field=models.BooleanField(default=False),
        ),
    ]
