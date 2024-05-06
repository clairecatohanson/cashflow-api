from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from cashflowapi.models import Group
from cashflowapi.serializers import GroupSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def retrieve(self, request, pk=None):
        group = get_object_or_404(Group, pk=pk)
        serializer = GroupSerializer(group)
        return Response(serializer.data)

    def list(self, request):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        group = get_object_or_404(Group, pk=pk)

        # Get keys from the request body
        name = request.data.get("name", None)

        if not name:
            return Response(
                {
                    "error": "Missing required fields. Please include at least one of the following: name."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update and save the instance
        group.name = name
        group.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        # Check for required keys in the request body
        name = request.data.get("name", None)

        if not name:
            return Response(
                {
                    "error": "Missing required fields. Please include at least one of the following: name."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create a new instance
        try:
            group = Group.objects.create(name=name)
        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = GroupSerializer(group, many=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk=None):
        group = get_object_or_404(Group, pk=pk)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
