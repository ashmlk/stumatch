# Generated by Django 3.0 on 2020-03-08 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='profile_image/profile_default.png', upload_to='profile_image'),
        ),
    ]
