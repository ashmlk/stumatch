# Generated by Django 3.0 on 2020-06-30 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_auto_20200629_0413'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searchlog',
            name='user',
        ),
        migrations.AddField(
            model_name='profile',
            name='recent_searches',
            field=models.ManyToManyField(related_name='recent_searches', to='main.SearchLog'),
        ),
    ]
