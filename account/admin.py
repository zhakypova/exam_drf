from django.contrib import admin

# Register your models here.

from .models import Author, User

admin.site.register(Author)
admin.site.register(User)