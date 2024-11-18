from django.db import models
from django.contrib.auth.models import AbstractUser
from A_B_test.test_config import variants
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    is_manager = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    REQUIRED_FIELDS = ['email']


class Rating(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    item_id = models.CharField(max_length=10)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    objects = models.Manager()

    class Meta:
        ordering = ['user']

    def __str__(self):
        return self.item_id


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
