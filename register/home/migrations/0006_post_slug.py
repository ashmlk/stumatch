# Generated by Django 3.0 on 2020-03-07 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0005_auto_20200306_2013"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="slug",
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
