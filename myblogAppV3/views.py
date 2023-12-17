from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *


# Create your views here.
# LOGOUT = logging
def logout_view(request):
    logout(request)
    return redirect("/")


# LOGIN = login
def login_view(request):
    return render(request, "login.html")


# HOME PAGE


def home(request):
    context = {"blogs": BlogModel.objects.all()}
    return render(request, "home.html", context)


# ABOUT US PAGE
def about(request):
    context = {"blogs": BlogModel.objects.all()}
    return render(request, "about.html", context)


def register_view(request):
    return render(request, "register.html")
    return redirect("/login")


def blog_detail(request, slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.filter(slug=slug).first()
        context["blog_obj"] = blog_obj
    except Exception as e:
        print(e)
    return render(request, "blog_detail.html")


# ADD BLOG
def add_blog(request):
    context = {"form": BlogForm}
    try:
        if request.method == "POST":
            form = BlogForm(request.POST)
            print(request.FILES)
            image = request.FILES["image"]
            title = request.POST.get("title")
            user = (
                request.user
            )  # This Area is printing(NOT NULL constraint failed: myblogAppV3_blogmodel.author_id)

            if form.is_valid():
                content = form.cleaned_data["content"]

            blog_obj = BlogModel.objects.create(
                user=user, title=title, content=content, image=image
            )
            print(blog_obj)
            return redirect("/add-blog")

    except Exception as e:
        print(e)
    return render(request, "add_blog.html", context)


# BLOG DETAILS
def blog_detail(request, slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.filter(slug=slug).first()
        context["blog_obj"] = blog_obj
    except Exception as e:
        print(e)
    return render(request, "blog_detail.html", context)


# BLOG VIEWS
def see_blog(request):
    context = {}
    try:
        blog_objs = BlogModel.objects.filter(user=request.user)
        context["blog_objs"] = blog_objs
    except Exception as e:
        print(e)
    return render(request, "see_blog.html", context)


# UPDATE BLOG
def blog_update(request, slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.get(slug=slug)

        if blog_obj.user != request.user:
            return redirect("/")  # TODO: handle redirect

        initial_dict = {"content": blog_obj.content}
        form = BlogForm(initial=initial_dict)
        if request.method == "POST":
            form = BlogForm(request.POST)
            print(request.FILES)
            image = request.FILES["image"]
            title = request.POST.get("title")
            user = request.user

            if form.is_valid():
                content = form.cleaned_data["content"]

            blog_obj = BlogModel.objects.create(
                user=user, title=title, content=content, image=image
            )

        context["blog_obj"] = blog_obj
        context["form"] = form
    except Exception as e:
        print(e)
    return render(request, "update_blog.html", context)


# DELETING BLOG
def blog_delete(request, id):
    try:
        blog_obj = BlogModel.objects.get(id=id)
        if blog_obj.user == request.user:
            blog_obj.delete()
    except Exception as e:
        print(e)
    return redirect("/see-blog")


def verify(request, token):
    try:
        profile_obj = Profile.objects.filter(token=token).first()

        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
        return redirect("/login")
    except Exception as e:
        print(e)
    return redirect("/")


# TITLE BLOG FUNCTIONS
class PageTitleViewMixin:
    context = {"title": "Profile"}
    title = ""

    def get_title(self):
        """
        Return the class title attr by default,
        but you can override this method to further customize
        """
        return self.title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_title()
        return context
