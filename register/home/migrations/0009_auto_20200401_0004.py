# Generated by Django 3.0 on 2020-04-01 00:04

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0008_images'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created_on']},
        ),
        migrations.AddField(
            model_name='course',
            name='course_dislikes',
            field=models.ManyToManyField(blank=True, related_name='course_dislikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='course_likes',
            field=models.ManyToManyField(blank=True, related_name='course_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_code',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_instructor',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_semester',
            field=models.CharField(choices=[('1', 'Spring'), ('2', 'Summer'), ('3', 'Fall'), ('4', 'Winter'), ('0', 'None')], default='0', max_length=2),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_university',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='images',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(validators=[django.core.validators.MaxLengthValidator(700)]),
        ),
    ]