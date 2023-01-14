from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    patronymic = models.CharField(max_length=20, null=True, blank=True)


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username



