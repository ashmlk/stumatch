# Generated by Django 3.0 on 2020-06-26 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_delete_friendrequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='friends',
        ),
    ]
