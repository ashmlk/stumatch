# Generated by Django 3.0 on 2020-03-06 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0004_auto_20200306_1949"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post", old_name="pub_date", new_name="date_posted",
        ),
    ]
