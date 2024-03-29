# Generated by Django 3.0 on 2021-01-03 00:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0072_auto_20201230_1619"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="course_year",
            field=models.IntegerField(
                validators=[
                    django.core.validators.MinValueValidator(1984),
                    django.core.validators.MaxValueValidator(2022),
                ],
                verbose_name="year",
            ),
        ),
        migrations.AlterField(
            model_name="courselist",
            name="year",
            field=models.IntegerField(
                blank=True,
                validators=[
                    django.core.validators.MinValueValidator(1984),
                    django.core.validators.MaxValueValidator(2022),
                ],
                verbose_name="year",
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="year",
            field=models.IntegerField(
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1984),
                    django.core.validators.MaxValueValidator(2022),
                ],
                verbose_name="year",
            ),
        ),
    ]
