from rest_framework import serializers
from django.contrib.auth.models import User
from cashflowapi.models import Group, Category, Team, UserTeam, Expense, Payment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name")


class UserTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTeam
        fields = "__all__"


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"


class UserTeamSerializerExpanded(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    team = TeamSerializer(many=False)

    class Meta:
        model = UserTeam
        fields = "__all__"


class UserSerializerEmbedded(serializers.ModelSerializer):
    user_teams = UserTeamSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "user_teams")


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"


class ExpenseSerializerExpanded(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    user = UserSerializer(many=False)
    team = TeamSerializer(many=False)

    class Meta:
        model = Expense
        fields = "__all__"


class ExpenseSerializerEmbedded(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True)

    class Meta:
        model = Expense
        fields = (
            "id",
            "date",
            "description",
            "amount",
            "category",
            "user",
            "team",
            "payments",
        )


class ExpenseSerializerExpandedAndEmbedded(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    user = UserSerializer(many=False)
    team = TeamSerializer(many=False)
    payments = PaymentSerializer(many=True)

    class Meta:
        model = Expense
        fields = (
            "id",
            "date",
            "description",
            "amount",
            "category",
            "user",
            "team",
            "payments",
        )
