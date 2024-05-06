from django.db import models
from django.contrib.auth.models import User


class Payment(models.Model):
    expense = models.ForeignKey(
        "Expense", on_delete=models.CASCADE, related_name="payments"
    )
    amount = models.FloatField()
    datePaid = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
