from django.contrib import admin

# Register your models here.

from .models import Profile, Post, Photo

#Register The models into the database
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)