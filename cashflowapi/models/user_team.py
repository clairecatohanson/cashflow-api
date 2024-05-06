from django.db import models
from django.contrib.auth.models import User


class UserTeam(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_teams")
    splitFraction = models.FloatField()
    team = models.ForeignKey(
        "Team", on_delete=models.CASCADE, related_name="user_teams"
    )
