# Generated by Django 3.0 on 2020-06-29 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0020_searchlog"),
    ]

    operations = [
        migrations.AlterField(
            model_name="searchlog",
            name="search_text",
            field=models.TextField(db_index=True),
        ),
    ]
