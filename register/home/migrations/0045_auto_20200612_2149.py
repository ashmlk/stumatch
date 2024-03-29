# Generated by Django 3.0 on 2020-06-12 21:49

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ("taggit", "0003_taggeditem_add_unique_index"),
        ("home", "0044_auto_20200612_2148"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blog",
            name="tags",
            field=taggit.managers.TaggableManager(
                blank=True,
                help_text="Tags",
                through="taggit.TaggedItem",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="tags",
            field=taggit.managers.TaggableManager(
                blank=True,
                help_text="Tags",
                through="taggit.TaggedItem",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
    ]
