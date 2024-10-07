from django.db import models
from django.contrib.auth.models import AbstractUser
from A_B_test_project.config import VARIANTS


class User(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    REQUIRED_FIELDS = []


class Item(models.Model):
    title = models.CharField(unique=True, max_length=50)
    description = models.CharField(null=True, max_length=250)
    score = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ModelAssignment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    recommendations_model = models.CharField(max_length=1, choices=VARIANTS, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user']

    def __str__(self):
        return self.recommendations_model
