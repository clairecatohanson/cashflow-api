from django.db import models
from django.contrib.auth.models import User


class UserTeam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_teams")
    splitFraction = models.FloatField()
    team = models.ForeignKey(
        "Team", on_delete=models.CASCADE, related_name="user_teams"
    )
