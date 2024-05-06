from django.db import models
from django.contrib.auth.models import User


class Expense(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateField()
    description = models.CharField(max_length=255)
    amount = models.FloatField()
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="expenses"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    team = models.ForeignKey("Team", on_delete=models.CASCADE, related_name="expenses")
