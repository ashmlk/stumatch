# Generated by Django 3.0 on 2020-11-17 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0065_review_is_anonymous'),
    ]

    operations = [
        migrations.AddField(
            model_name='professors',
            name='courses',
            field=models.ManyToManyField(related_name='instructor_courses', to='home.Course'),
        ),
    ]
