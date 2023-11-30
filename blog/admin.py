from django.contrib import admin
from .models import BlogPost, BlogComment

# Register your models here.

admin.site.register(BlogComment)
admin.site.register(BlogPost)