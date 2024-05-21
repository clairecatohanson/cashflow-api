from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from cashflowapi.models import Expense, Category, Team
from cashflowapi.serializers import (
    ExpenseSerializer,
    ExpenseSerializerExpanded,
    ExpenseSerializerEmbedded,
    ExpenseSerializerExpandedAndEmbedded,
)


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def create(self, request):
        # Get user
        user = request.auth.user

        # Check for required keys in the request body
        date = request.data.get("date", None)
        description = request.data.get("description", None)
        amount = request.data.get("amount", None)
        category_id = request.data.get("categoryId", None)
        team_id = request.data.get("team_Id", None)

        if not date or not description or not amount or not category_id or not team_id:
            return Response(
                {
                    "error": "Missing required fields. Please include date, description, amount, categoryId, and team_Id."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        category = get_object_or_404(Category, pk=category_id)
        team = get_object_or_404(Team, pk=team_id)

        # Create a new instance
        try:
            expense = Expense.objects.create(
                date=date,
                description=description,
                amount=amount,
                category=category,
                team=team,
                user=user,
            )
        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ExpenseSerializer(expense, many=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        expense = get_object_or_404(Expense, pk=pk)

        # Get keys from the request body
        date = request.data.get("date", None)
        description = request.data.get("description", None)
        amount = request.data.get("amount", None)
        category_id = request.data.get("categoryId", None)
        team_id = request.data.get("team_Id", None)

        if (
            not date
            and not description
            and not amount
            and not category_id
            and not team_id
        ):
            return Response(
                {
                    "error": "Missing required fields. Please include date, description, amount, categoryId, or team_Id."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update and save the instance
        if date is not None:
            expense.date = date

        if description is not None:
            expense.description = description

        if amount is not None:
            expense.amount = amount

        if category_id is not None:
            category = get_object_or_404(Category, pk=category_id)
            expense.category = category

        if team_id is not None:
            team = get_object_or_404(Team, pk=team_id)
            expense.team = team

        expense.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk=None):
        expense = get_object_or_404(Expense, pk=pk)
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        expenses = Expense.objects.all()

        # get optional query params
        team_id = request.query_params.get("team_Id", None)
        expand = request.query_params.get("_expand", None)
        embed = request.query_params.get("_embed", None)

        # filter by team
        if team_id is not None:
            team = get_object_or_404(Team, pk=team_id)
            expenses = expenses.filter(team=team)

        serializer = ExpenseSerializer(expenses, many=True)

        # select appropriate expand/embed serializer
        if expand is not None:
            if embed is not None:
                serializer = ExpenseSerializerExpandedAndEmbedded(expenses, many=True)
            else:
                serializer = ExpenseSerializerExpanded(expenses, many=True)

        if embed is not None:
            if expand is not None:
                serializer = ExpenseSerializerExpandedAndEmbedded(expenses, many=True)
            else:
                serializer = ExpenseSerializerEmbedded(expenses, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        expense = get_object_or_404(Expense, pk=pk)
        serializer = ExpenseSerializer(expense, many=False)

        # get optional query params
        expand = request.query_params.get("_expand", None)
        embed = request.query_params.get("_embed", None)

        # select appropriate expand/embed serializer
        if expand is not None:
            if embed is not None:
                serializer = ExpenseSerializerExpandedAndEmbedded(expense, many=False)
            else:
                serializer = ExpenseSerializerExpanded(expense, many=False)

        if embed is not None:
            if expand is not None:
                serializer = ExpenseSerializerExpandedAndEmbedded(expense, many=False)
            else:
                serializer = ExpenseSerializerEmbedded(expense, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)
