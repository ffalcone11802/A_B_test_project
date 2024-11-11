from django.db import models
from django.contrib.auth.models import AbstractUser
from A_B_test_project.config import variants


class User(AbstractUser):
    is_manager = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    REQUIRED_FIELDS = ['email']


class Rating(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    item_id = models.CharField(max_length=10)
    rating = models.IntegerField(default=0)

    objects = models.Manager()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.user_id


"""class Item(models.Model):
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
        return self.name"""


class VariantAssignment(models.Model):
    rec_vars = [(k, k) for k in variants.keys()]

    user = models.ForeignKey("User", on_delete=models.CASCADE)
    variant = models.CharField(max_length=10, choices=rec_vars, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        ordering = ['user']

    def __str__(self):
        return self.variant
