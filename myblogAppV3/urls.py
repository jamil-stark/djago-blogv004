from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("about-us/", about, name="about"),
    path("login/", login_view, name="login_view"),
    path("logout-user/", logout_view, name="logout_user"),
    path("register/", register_view, name="register"),
    path("add-blog/", add_blog, name="add_blog"),
    path("blog-detail/<slug>", blog_detail, name="blog_detail"),
    path("see-blog/", see_blog, name="see_blog"),
    path("blog-delete/<id>", blog_delete, name="blog_delete"),
    path("blog-update/<slug>/", blog_update, name="blog_update"),
    path("verify/<token>", verify, name="verify"),
]
