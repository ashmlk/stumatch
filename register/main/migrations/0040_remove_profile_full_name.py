# Generated by Django 3.0 on 2021-01-07 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_profile_full_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='full_name',
        ),
    ]