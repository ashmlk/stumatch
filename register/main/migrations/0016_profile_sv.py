# Generated by Django 3.0 on 2020-06-28 01:48

import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0015_auto_20200628_0136"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="sv",
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
    ]
