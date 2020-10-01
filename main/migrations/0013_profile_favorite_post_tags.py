# Generated by Django 3.0 on 2020-06-27 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('main', '0012_remove_profile_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='favorite_post_tags',
            field=models.ManyToManyField(related_name='fav_Post_tags', to='taggit.Tag'),
        ),
    ]
