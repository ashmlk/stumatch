# Generated by Django 3.0 on 2020-08-30 23:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0058_courselistobjects_created_on"),
        ("main", "0031_profile_get_friendrequestaccepted_notify"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="profile", managers=[("objects", main.models.ProfileManager()),],
        ),
        migrations.CreateModel(
            name="ReportUser",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_reported", models.DateTimeField(auto_now_add=True)),
                (
                    "reason",
                    models.CharField(
                        choices=[
                            ("not_interested", "Not Interested in this content"),
                            ("spam", "It appears to be spam"),
                            ("sensitive", "It displays sensitive content"),
                            ("harmful", "I find it abusive or harmful"),
                            (
                                "self_harm",
                                "It display and portrays expression of self-harm or suicide",
                            ),
                            (
                                "hate",
                                "It appears to be inflammatory speech towards a demographic",
                            ),
                            ("misleading", "It appears to share misleading content"),
                            ("threat", "It is threatening and expressing violent harm"),
                            ("null", "None"),
                        ],
                        default="null",
                        max_length=250,
                    ),
                ),
                (
                    "reported_obj",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reported_users",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="report_user",
                    ),
                ),
                (
                    "reporter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="ReportPost",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_reported", models.DateTimeField(auto_now_add=True)),
                (
                    "reason",
                    models.CharField(
                        choices=[
                            ("not_interested", "Not Interested in this content"),
                            ("spam", "It appears to be spam"),
                            ("sensitive", "It displays sensitive content"),
                            ("harmful", "I find it abusive or harmful"),
                            (
                                "self_harm",
                                "It display and portrays expression of self-harm or suicide",
                            ),
                            (
                                "hate",
                                "It appears to be inflammatory speech towards a demographic",
                            ),
                            ("misleading", "It appears to share misleading content"),
                            ("threat", "It is threatening and expressing violent harm"),
                            ("null", "None"),
                        ],
                        default="null",
                        max_length=250,
                    ),
                ),
                (
                    "reported_obj",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reported_posts",
                        to="home.Post",
                        verbose_name="report_post",
                    ),
                ),
                (
                    "reporter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="ReportCourseReview",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_reported", models.DateTimeField(auto_now_add=True)),
                (
                    "reason",
                    models.CharField(
                        choices=[
                            ("not_interested", "Not Interested in this content"),
                            ("spam", "It appears to be spam"),
                            ("sensitive", "It displays sensitive content"),
                            ("harmful", "I find it abusive or harmful"),
                            (
                                "self_harm",
                                "It display and portrays expression of self-harm or suicide",
                            ),
                            (
                                "hate",
                                "It appears to be inflammatory speech towards a demographic",
                            ),
                            ("misleading", "It appears to share misleading content"),
                            ("threat", "It is threatening and expressing violent harm"),
                            ("null", "None"),
                        ],
                        default="null",
                        max_length=250,
                    ),
                ),
                (
                    "reported_obj",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reported_coursereviews",
                        to="home.Review",
                        verbose_name="report_coursereview",
                    ),
                ),
                (
                    "reporter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="ReportComment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_reported", models.DateTimeField(auto_now_add=True)),
                (
                    "reason",
                    models.CharField(
                        choices=[
                            ("not_interested", "Not Interested in this content"),
                            ("spam", "It appears to be spam"),
                            ("sensitive", "It displays sensitive content"),
                            ("harmful", "I find it abusive or harmful"),
                            (
                                "self_harm",
                                "It display and portrays expression of self-harm or suicide",
                            ),
                            (
                                "hate",
                                "It appears to be inflammatory speech towards a demographic",
                            ),
                            ("misleading", "It appears to share misleading content"),
                            ("threat", "It is threatening and expressing violent harm"),
                            ("null", "None"),
                        ],
                        default="null",
                        max_length=250,
                    ),
                ),
                (
                    "reported_obj",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reported_comments",
                        to="home.Comment",
                        verbose_name="report_comment",
                    ),
                ),
                (
                    "reporter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="ReportBuzzReply",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_reported", models.DateTimeField(auto_now_add=True)),
                (
                    "reason",
                    models.CharField(
                        choices=[
                            ("not_interested", "Not Interested in this content"),
                            ("spam", "It appears to be spam"),
                            ("sensitive", "It displays sensitive content"),
                            ("harmful", "I find it abusive or harmful"),
                            (
                                "self_harm",
                                "It display and portrays expression of self-harm or suicide",
                            ),
                            (
                                "hate",
                                "It appears to be inflammatory speech towards a demographic",
                            ),
                            ("misleading", "It appears to share misleading content"),
                            ("threat", "It is threatening and expressing violent harm"),
                            ("null", "None"),
                        ],
                        default="null",
                        max_length=250,
                    ),
                ),
                (
                    "reported_obj",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reported_buzzreplies",
                        to="home.BuzzReply",
                        verbose_name="report_buzzreply",
                    ),
                ),
                (
                    "reporter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="ReportBuzz",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_reported", models.DateTimeField(auto_now_add=True)),
                (
                    "reason",
                    models.CharField(
                        choices=[
                            ("not_interested", "Not Interested in this content"),
                            ("spam", "It appears to be spam"),
                            ("sensitive", "It displays sensitive content"),
                            ("harmful", "I find it abusive or harmful"),
                            (
                                "self_harm",
                                "It display and portrays expression of self-harm or suicide",
                            ),
                            (
                                "hate",
                                "It appears to be inflammatory speech towards a demographic",
                            ),
                            ("misleading", "It appears to share misleading content"),
                            ("threat", "It is threatening and expressing violent harm"),
                            ("null", "None"),
                        ],
                        default="null",
                        max_length=250,
                    ),
                ),
                (
                    "reported_obj",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reported_buzzes",
                        to="home.Buzz",
                        verbose_name="report_buzz",
                    ),
                ),
                (
                    "reporter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="ReportBlogReply",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_reported", models.DateTimeField(auto_now_add=True)),
                (
                    "reason",
                    models.CharField(
                        choices=[
                            ("not_interested", "Not Interested in this content"),
                            ("spam", "It appears to be spam"),
                            ("sensitive", "It displays sensitive content"),
                            ("harmful", "I find it abusive or harmful"),
                            (
                                "self_harm",
                                "It display and portrays expression of self-harm or suicide",
                            ),
                            (
                                "hate",
                                "It appears to be inflammatory speech towards a demographic",
                            ),
                            ("misleading", "It appears to share misleading content"),
                            ("threat", "It is threatening and expressing violent harm"),
                            ("null", "None"),
                        ],
                        default="null",
                        max_length=250,
                    ),
                ),
                (
                    "reported_obj",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reported_blogreplies",
                        to="home.BlogReply",
                        verbose_name="report_blogreply",
                    ),
                ),
                (
                    "reporter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="ReportBlog",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_reported", models.DateTimeField(auto_now_add=True)),
                (
                    "reason",
                    models.CharField(
                        choices=[
                            ("not_interested", "Not Interested in this content"),
                            ("spam", "It appears to be spam"),
                            ("sensitive", "It displays sensitive content"),
                            ("harmful", "I find it abusive or harmful"),
                            (
                                "self_harm",
                                "It display and portrays expression of self-harm or suicide",
                            ),
                            (
                                "hate",
                                "It appears to be inflammatory speech towards a demographic",
                            ),
                            ("misleading", "It appears to share misleading content"),
                            ("threat", "It is threatening and expressing violent harm"),
                            ("null", "None"),
                        ],
                        default="null",
                        max_length=250,
                    ),
                ),
                (
                    "reported_obj",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reported_blogs",
                        to="home.Blog",
                        verbose_name="report_blog",
                    ),
                ),
                (
                    "reporter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
    ]
