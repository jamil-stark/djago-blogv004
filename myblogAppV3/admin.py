from django.contrib import admin

# Register your models here.
from .models import *


class BlogModelAdmin(admin.ModelAdmin):
    list_display = ["title", "content", "user"]


admin.site.register(BlogModel, BlogModelAdmin)
admin.site.register(Profile)
