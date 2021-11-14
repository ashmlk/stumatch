# Generated by Django 3.0 on 2021-01-07 20:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0041_profile_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='full_name',
            field=models.TextField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(300)]),
        ),
    ]