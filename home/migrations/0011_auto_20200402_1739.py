# Generated by Django 3.0 on 2020-04-02 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20200402_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.FileField(upload_to='post_images/'),
        ),
    ]
