# Generated by Django 3.0 on 2020-04-09 18:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0019_auto_20200406_0615"),
    ]

    operations = [
        migrations.RenameField(model_name="images", old_name="file", new_name="image",),
        migrations.AlterField(
            model_name="post",
            name="content",
            field=models.TextField(
                validators=[django.core.validators.MaxLengthValidator(1200)]
            ),
        ),
    ]
