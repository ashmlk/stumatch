# Generated by Django 3.0 on 2020-08-23 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_profile_save_searches'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='get_blog_notify_all',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='get_blog_notify_comments',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='get_blog_notify_likes',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='get_buzz_notify_all',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='get_buzz_notify_likes',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='get_buzz_notify_replies',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='get_friendrequest_notify',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='get_notify',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='get_post_notify_all',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='get_post_notify_comments',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='get_post_notify_likes',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]