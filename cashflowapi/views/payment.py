from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from cashflowapi.models import Payment, Expense
from cashflowapi.serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def list(self, request):
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        payment = get_object_or_404(Payment, pk=pk)
        payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        # Get user
        user = request.auth.user

        # Check for required keys in the request body
        expense_id = request.data.get("expenseId", None)
        amount = request.data.get("amount", None)
        datePaid = request.data.get("datePaid", None)

        if not expense_id or not amount or not datePaid:
            return Response(
                {
                    "error": "Missing required fields. Please include expense_id, amount, and datePaid."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        expense = get_object_or_404(Expense, pk=expense_id)

        # Create a new instance
        try:
            payment = Payment.objects.create(
                expense=expense,
                amount=amount,
                datePaid=datePaid,
                user=user,
            )
        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PaymentSerializer(payment, many=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
