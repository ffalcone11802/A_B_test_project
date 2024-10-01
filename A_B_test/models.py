from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(null=False, blank=False, max_length=20)
    last_name = models.CharField(null=False, blank=False, max_length=20)

    class Meta:
        ordering = ['username']

    REQUIRED_FIELDS = []


class Item(models.Model):
    title = models.CharField(null=False, blank=False, max_length=50)
    description = models.CharField(null=True, max_length=250)

    def __str__(self):
        return self.title


class ModelAssignment(models.Model):
    hashed_user_id = models.CharField(null=False, blank=False)
    recommendations_model = models.CharField(null=True, default=None)

    class Meta:
        ordering = ['hashed_user_id']


class Variant(models.Model):
    name = models.CharField(null=False, blank=False)

    class Meta:
        ordering = ['name']
