# Generated by Django 3.0 on 2020-04-06 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_auto_20200405_0602'),
    ]

    operations = [
        migrations.RenameField(
            model_name='images',
            old_name='image',
            new_name='file',
        ),
    ]