# Generated by Django 3.1.5 on 2021-01-07 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0042_auto_20210107_2058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='image',
        ),
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
