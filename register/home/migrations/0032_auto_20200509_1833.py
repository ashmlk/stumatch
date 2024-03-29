# Generated by Django 3.0 on 2020-05-09 18:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("home", "0031_auto_20200509_0415"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="dislikes",
            field=models.ManyToManyField(
                blank=True, related_name="review_dislikes", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="review",
            name="review_interest",
            field=models.CharField(
                choices=[
                    ("1", "Interesting"),
                    ("2", "Relatively Interesting"),
                    ("3", "Not Interesting"),
                    ("4", "No opinion"),
                ],
                default="4",
                max_length=2,
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="guid_url",
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]
