from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from cashflowapi.models import UserTeam, Team
from cashflowapi.serializers import UserTeamSerializer, UserTeamSerializerExpanded


class UserTeamViewSet(viewsets.ModelViewSet):
    queryset = UserTeam.objects.all()
    serializer_class = UserTeamSerializer

    def create(self, request):
        # Check for required keys in the request body
        user_id = request.data.get("userId", None)
        team_id = request.data.get("teamId", None)
        splitFraction = request.data.get("splitFraction", None)

        if not user_id or not team_id or not splitFraction:
            return Response(
                {
                    "error": "Missing required fields. Please include userId, teamId, and splitFraction."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = get_object_or_404(User, pk=user_id)
        team = get_object_or_404(Team, pk=team_id)

        # Create a new instance
        try:
            userteam = UserTeam.objects.create(
                user=user, team=team, splitFraction=splitFraction
            )
        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserTeamSerializer(userteam, many=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk=None):
        userteam = get_object_or_404(UserTeam, pk=pk)
        userteam.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        userteams = UserTeam.objects.all()

        # get optional query params
        user_id = request.query_params.get("userId", None)
        team_id = request.query_params.get("teamId", None)
        expand = request.query_params.get("_expand", None)

        # filter by user
        if user_id is not None:
            user = get_object_or_404(User, pk=user_id)
            userteams = userteams.filter(user=user)

        # filter by team
        if team_id is not None:
            team = get_object_or_404(Team, pk=team_id)
            userteams = userteams.filter(team=team)

        serializer = UserTeamSerializer(userteams, many=True)

        # select appropriate expand/embed serializer
        if expand is not None:
            serializer = UserTeamSerializerExpanded(userteams, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
