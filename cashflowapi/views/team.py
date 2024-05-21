from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from cashflowapi.models import Team
from cashflowapi.serializers import TeamSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def create(self, request):
        # Check for required keys in the request body
        name = request.data.get("name", None)

        if not name:
            return Response(
                {"error": "Missing required fields. Please include name."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create a new instance
        try:
            team = Team.objects.create(name=name)
        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TeamSerializer(team, many=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        team = get_object_or_404(Team, pk=pk)

        # Get keys from the request body
        name = request.data.get("name", None)

        if not name:
            return Response(
                {"error": "Missing required fields. Please include name."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update and save the instance
        if name is not None:
            team.name = name

        team.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk=None):
        team = get_object_or_404(Team, pk=pk)
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        team = get_object_or_404(Team, pk=pk)
        serializer = TeamSerializer(team)
        return Response(serializer.data, status=status.HTTP_200_OK)
