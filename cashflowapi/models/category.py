from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    group = models.ForeignKey(
        "Group", on_delete=models.CASCADE, related_name="categories"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
