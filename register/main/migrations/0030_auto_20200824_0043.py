# Generated by Django 3.0 on 2020-08-24 00:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_auto_20200823_2316'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='get_buzz_notify_replies',
            new_name='get_buzz_notify_comments',
        ),
    ]
