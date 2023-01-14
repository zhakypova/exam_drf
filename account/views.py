from rest_framework import generics, status
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Author
from .seriallizers import AuthorSerializer


class AuthorRegisterView(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer




