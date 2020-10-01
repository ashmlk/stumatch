# Generated by Django 3.0 on 2020-06-22 02:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0046_auto_20200615_2236'),
        ('main', '0009_profile_saved_courses'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookmarkPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Post', verbose_name='Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'db_table': 'bookmark_post',
            },
        ),
        migrations.CreateModel(
            name='BookmarkBuzz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Buzz', verbose_name='Buzz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'db_table': 'bookmark_buzz',
            },
        ),
        migrations.CreateModel(
            name='BookmarkBlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Blog', verbose_name='Blog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'db_table': 'bookmark_blog',
            },
        ),
    ]