# Generated by Django 3.0 on 2020-09-23 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0059_course_course_instructor_fn'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_prof_difficulty',
            field=models.CharField(blank=True, choices=[('0', 'TBD'), ('1', 'Easy'), ('2', 'Medium'), ('3', 'Hard'), ('4', 'Failed')], default='0', max_length=2),
        ),
    ]