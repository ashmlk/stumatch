from django.contrib import admin
from .models import Post, Comment, Images, Course, Review, Buzz, BuzzReply, Blog, BlogReply
# Register your models here.
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Images)
admin.site.register(Course)
admin.site.register(Review)
admin.site.register(Buzz)
admin.site.register(BuzzReply)
admin.site.register(Blog)
admin.site.register(BlogReply)