# Generated by Django 3.0 on 2020-05-02 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0023_comment_likes"),
        ("main", "0007_profile_courses"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="courses",
            field=models.ManyToManyField(related_name="profiles", to="home.Course"),
        ),
    ]
