# Generated by Django 3.0 on 2020-07-06 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0022_auto_20200630_1846"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="public",
            field=models.BooleanField(default=False),
        ),
    ]
