# Generated by Django 3.0 on 2020-05-16 17:30

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0038_auto_20200516_1723'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuzzReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply_nickname', models.CharField(blank=True, max_length=30, null=True)),
                ('reply_content', models.TextField(validators=[django.core.validators.MaxLengthValidator(180)])),
                ('date_replied', models.DateTimeField(auto_now_add=True)),
                ('buzz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='breplies', to='home.Buzz')),
                ('reply_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('reply_dislikes', models.ManyToManyField(blank=True, related_name='rdilikes', to=settings.AUTH_USER_MODEL)),
                ('reply_likes', models.ManyToManyField(blank=True, related_name='rlikes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]