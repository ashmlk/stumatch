# Generated by Django 3.0 on 2020-05-10 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0032_auto_20200509_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_university_slug',
            field=models.SlugField(blank=True, max_length=250, null=True),
        ),
    ]
