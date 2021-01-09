from django.conf.urls import url
from django.urls import path, include
from main import views
from django.contrib.auth import views as auth_views
from defender.decorators import watch_login
from .models import BookmarkBlog, BookmarkBuzz, BookmarkPost
from django.conf.urls import handler400, handler403, handler404, handler500
from django.contrib.sitemaps.views import sitemap
from main.sitemaps import StaticViewSitemap

sitemaps = {"static": StaticViewSitemap}
handler404 = "main.views.handle_404"
# handler500 = 'main.views.handle_500'
# handler403 = 'main.views.handle_403'
# handler400 = 'main.views.handle_400'
# SET THE NAMESPACE!
app_name = "main"

urlpatterns = [
    path(
        "spofnv394hp9hwb0werh3w3w0r9vw-qi3r9h-wiepvhAER-QWRIOEw89hABVP.xml",
        sitemap,
        {"sitemaps": sitemaps},
    ),
    path("policies/data/", views.policy_html, name="web-policy"),
    path("policies/cookies/", views.cookies_html, name="cookies-policy"),
    path("terms/", views.terms_html, name="site-terms"),
    path("about/", views.about_html, name="site-about"),
    path("contact/", views.contact_us, name="contact-us"),
    path("signup/", views.signup, name="signup"),
    path("validate_signup", views.validate_and_check_signup, name="validate-username"),
    path("", views.user_login, name="user_login"),
    path(
        "update/email/signup/action/",
        views.update_user_email_on_verification,
        name="update-user-email-signup",
    ),
    path("signout", views.user_logout, name="user_logout"),
    path("report/submit/<str:reporter_id>", views.report_object, name="report-object"),
    path("settings/edit/profile/", views.edit_profile, name="settings-edit"),
    path("update/profile/data/", views.edit_profile_data, name="update-profile-data"),
    path(
        "update/profile/university/",
        views.edit_profile_university,
        name="update-profile-university",
    ),
    path("update/add/university/", views.add_university, name="update-university"),
    path("update/profile/image/<str:hid>/", views.update_image, name="update-image"),
    path("remove/profile/image/<str:hid>/", views.remove_image, name="remove-image"),
    path("settings/privacy/", views.privacy_security, name="privacy-security"),
    path(
        "settings/security/profile/",
        views.set_public_private,
        name="set-public-private",
    ),
    path("settings/privacy/password/", views.change_password, name="change-password"),
    path("settings/security/search/", views.search_settings, name="search-settings"),
    path("settings/security/data/manage/", views.deletion_menu, name="delete-menu"),
    path("settings/security/data/posts", views.deletion_post, name="post-deletion"),
    path("settings/security/data/blogs", views.deletion_blog, name="blog-deletion"),
    path(
        "settings/security/data/courses", views.deletion_course, name="course-deletion"
    ),
    path(
        "settings/security/data/profile",
        views.deletion_account,
        name="account-deletion",
    ),
    path(
        "settings/notifications/",
        views.notification_settings_all,
        name="notifications-settings-all",
    ),
    path(
        "settings/notifications/post/",
        views.notifications_post_all,
        name="notifications-settings-post",
    ),
    path(
        "settings/notifications/blog/",
        views.notifications_blog_all,
        name="notifications-settings-blog",
    ),
    path(
        "settings/notifications/friends/",
        views.notifications_friends_all,
        name="notifications-settings-friends",
    ),
    path("settings/login_info/", views.login_info, name="login-info"),
    path("settings/blocked/", views.get_blocking, name="settings-blocked"),
    path("u/<str:username>/", views.get_user, name="get_user"),
    path("u/friends", views.get_user_friends, name="get_user_friends"),
    path("u/posts", views.get_user_posts, name="get_user_posts"),
    path("u/blogs", views.get_user_blogs, name="get_user_blogs"),
    path("u/courses", views.get_user_courses, name="get_user_courses"),
    path("bookmarks/", views.bookmarks, name="bookmarks"),
    path("bookmark/<str:hid>/<str:obj_type>/", views.add_bookmark, name="add-bookmark"),
    path("tags/<str:username>/", views.user_tags, name="usertags"),
    path("tags/posts/fav/<slug:slug>", views.f_post_tag, name="fav-post-tag"),
    path("tags/blogs/fav/<slug:slug>", views.f_blog_tag, name="fav-blog-tag"),
    path("friends/", views.friends_main, name="friends-main"),
    path("find/program/", views.user_same_program, name="find-program"),
    path("friends/requests/", views.friend_requests, name="friend-requests"),
    path(
        "friends/requests/pending/",
        views.friend_pending_requests,
        name="friend-pending",
    ),
    path(
        "friends/request/<str:hid>/action/<str:s>",
        views.accept_reject_friend_request,
        name="accept-reject-friend-request",
    ),
    path("friends/<str:hid>/<str:s>/", views.add_remove_friend, name="add-rmv-friend"),
    path("block/<str:hid>/", views.block_user, name="block-user"),
    path("unblock/<str:hid>/", views.unblock_user, name="unblock-user"),
    path("your_notifications/", views.get_notifications, name="get-notifications"),
    path(
        "your_notifications/mark_as_read",
        views.mark_notification_as_read,
        name="mark-notification-as-read",
    ),
    path(
        "your_notifications/delete",
        views.delete_notification,
        name="delete-notification",
    ),
    path("get/user/mentions", views.get_user_mentions, name="get-user-mentions")
    # path('signup/complete',views.user_completesignup,name='user_completesignup'),
    # path('', include('django.contrib.auth.urls')),
]
