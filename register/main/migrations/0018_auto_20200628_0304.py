# Generated by Django 3.0 on 2020-06-28 03:04

from django.db import migrations
from django.contrib.postgres.operations import UnaccentExtension


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20200628_0238'),
    ]

    operations = [
        UnaccentExtension()
    ]