# Generated by Django 3.0 on 2020-05-13 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0036_auto_20200513_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='buzz',
            name='nickname',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
