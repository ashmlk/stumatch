# Generated by Django 3.1.5 on 2021-01-07 22:19

from django.db import migrations, models
import django_uuid_upload
import functools


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0043_auto_20210107_2218'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='defaults/user/default_u_i.png', upload_to=functools.partial(django_uuid_upload._upload_to_uuid_impl, *(), **{'make_dir': False, 'path': 'profile_image/profiles/', 'remove_qs': True})),
        ),
    ]
