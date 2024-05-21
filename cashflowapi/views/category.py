from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from cashflowapi.models import Category, Group
from cashflowapi.serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def retrieve(self, request, pk=None):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def list(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        category = get_object_or_404(Category, pk=pk)
        user = request.auth.user

        if not category.user == user:
            return Response(
                {"error": "You are not authorized to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Get keys from the request body
        name = request.data.get("name", None)
        group_id = request.data.get("groupId", None)

        if not name and not group_id:
            return Response(
                {
                    "error": "Missing required fields. Please include at least one of the following: name, groupId."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update and save the instance
        if name is not None:
            category.name = name
        if group_id is not None:
            group = get_object_or_404(Group, pk=group_id)
            category.group = group
        category.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        # Get user
        user = request.auth.user

        # Check for required keys in the request body
        name = request.data.get("name", None)
        group_id = request.data.get("groupId", None)

        if not name or not group_id:
            return Response(
                {
                    "error": "Missing required fields. Please include at least one of the following: name, groupId."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        group = get_object_or_404(Group, pk=group_id)

        # Create a new instance
        try:
            category = Category.objects.create(name=name, group=group, user=user)
        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CategorySerializer(category, many=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk=None):
        category = get_object_or_404(Category, pk=pk)
        user = request.auth.user

        if not category.user == user:
            return Response(
                {"error": "You are not authorized to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
