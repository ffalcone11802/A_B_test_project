from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_manager = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    REQUIRED_FIELDS = ['email']


class Item(models.Model):
    title = models.CharField(unique=True, max_length=50)
    description = models.CharField(null=True, max_length=250)
    score = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Variant(models.Model):
    name = models.CharField(unique=True, max_length=20)
    endpoint = models.CharField(unique=True, max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class VariantAssignment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    variant = models.ForeignKey("Variant", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        ordering = ['user']

    def __str__(self):
        return self.variant.name
