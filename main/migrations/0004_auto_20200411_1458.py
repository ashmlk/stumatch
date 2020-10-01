# Generated by Django 3.0 on 2020-04-11 14:58

from django.db import migrations, models
import django_uuid_upload
import functools


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_profile_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='profile_image/profile_default.png', upload_to=functools.partial(django_uuid_upload._upload_to_uuid_impl, *(), **{'make_dir': False, 'path': 'post_images/profiles/', 'remove_qs': True})),
        ),
    ]