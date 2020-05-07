# Generated by Django 3.0 on 2020-04-29 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_remove_course_users'),
        ('main', '0006_profile_program'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='courses',
            field=models.ManyToManyField(related_name='courses', to='home.Course'),
        ),
    ]