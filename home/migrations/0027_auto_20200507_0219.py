# Generated by Django 3.0 on 2020-05-07 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_auto_20200507_0218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_dislikes',
            field=models.ManyToManyField(blank=True, related_name='course_comments', to='home.Comment'),
        ),
    ]