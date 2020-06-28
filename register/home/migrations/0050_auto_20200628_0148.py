# Generated by Django 3.0 on 2020-06-28 01:48

import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0049_auto_20200628_0140'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='sv',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
        migrations.AddField(
            model_name='buzz',
            name='sv',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='sv',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='sv',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
    ]
