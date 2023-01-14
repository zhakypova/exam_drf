from django.contrib import admin
from django.urls import path, include

from .models import Author
from .views import AuthorRegisterView


urlpatterns = [
    path('api/account/register', AuthorRegisterView.as_view())
]
