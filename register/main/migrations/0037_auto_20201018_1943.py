# Generated by Django 3.0 on 2020-10-18 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0036_delete_notification"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="program",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
