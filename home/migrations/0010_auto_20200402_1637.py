# Generated by Django 3.0 on 2020-04-02 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20200401_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='home.Post'),
        ),
    ]
