from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    ADMIN = 'admin'
    MANAGER = 'manager'
    USER = 'user'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (MANAGER, 'Manager'),
        (USER, 'User'),
    ]
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    role = models.ForeignKey( Role, on_delete=models.SET_NULL, null=True, blank=True )
