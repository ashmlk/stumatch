# Generated by Django 3.0 on 2020-04-29 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_auto_20200414_0125"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="program",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
