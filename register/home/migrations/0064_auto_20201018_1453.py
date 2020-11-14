# Generated by Django 3.0 on 2020-10-18 14:53

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0063_auto_20201017_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='professors',
            name='sv',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
        migrations.AddIndex(
            model_name='professors',
            index=django.contrib.postgres.indexes.GinIndex(fields=['sv'], name='search_idx_professors'),
        ),
    ]