import decimal
import logging

from django.db import transaction
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from .serializers import WalletSerializer, WalletHolderSerializer, TransactionSerializer, WalletDetailSerializer
from .models import Wallet, WalletHolder, Transaction


class WalletViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = Wallet.objects.filter(holder__user=request.user)
        serializer = WalletSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        queryset = get_object_or_404(Wallet.objects.filter(holder__user=request.user), pk=pk)
        serializer = WalletDetailSerializer(queryset, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class WalletHolderViewSet(viewsets.ModelViewSet):
    model = WalletHolder
    serializer_class = WalletHolderSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WalletHolder.objects.filter(user=self.request.user)


class TransactionViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def __get_user_transactions(self, user: User) -> QuerySet:
        incomes = Transaction.objects.filter(receiver__holder__user=user)
        expenses = Transaction.objects.filter(sender__holder__user=user)
        all_transactions = incomes | expenses
        return all_transactions

    def list(self, request):
        transactions: QuerySet = self.__get_user_transactions(request.user)
        serializer = TransactionSerializer(transactions, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        transactions: QuerySet = self.__get_user_transactions(request.user)
        transaction: QuerySet = get_object_or_404(transactions, pk=pk)
        serializer = TransactionSerializer(transaction, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        with transaction.atomic():
            serializer = TransactionSerializer(data=request.data, context={"request": request})
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                logging.info(f"transaction saved: {serializer.validated_data}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except serializers.ValidationError as e:
                logging.exception(e)
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
