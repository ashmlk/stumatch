from django.contrib import admin
from .models import (
    Profile,
    BookmarkBase,
    BookmarkBlog,
    BookmarkBuzz,
    BookmarkPost,
    ReportBase,
    ReportBlog,
    ReportBuzz,
    ReportBlogReply,
    ReportBuzzReply,
    ReportComment,
    ReportUser,
    ReportCourseReview,
)

# Register your models here.
admin.site.register(Profile)
admin.site.register(BookmarkBlog)
admin.site.register(BookmarkBuzz)
admin.site.register(BookmarkPost)
admin.site.register(ReportCourseReview)
admin.site.register(ReportBlog)
admin.site.register(ReportBuzz)
admin.site.register(ReportBuzzReply)
admin.site.register(ReportBlogReply)
admin.site.register(ReportComment)
admin.site.register(ReportUser)
