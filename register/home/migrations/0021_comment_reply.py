# Generated by Django 3.0 on 2020-04-10 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0020_auto_20200409_1855"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="reply",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="replies",
                to="home.Comment",
            ),
        ),
    ]
