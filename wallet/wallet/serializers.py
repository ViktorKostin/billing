import logging

from django.contrib.auth.models import User
from django.db.models import F
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Wallet, WalletHolder, Transaction, Currency


class WalletSerializer(serializers.ModelSerializer):
    currency = serializers.SlugRelatedField(
        queryset=Currency.objects.all(),
        slug_field='code',
    )
    url = serializers.HyperlinkedIdentityField(
        many=False,
        view_name='wallet:wallets-detail',
        read_only=True,
    )
    holder = serializers.SlugRelatedField(
        queryset=WalletHolder.objects.all(),
        slug_field='user__username',
    )

    class Meta:
        model = Wallet
        fields = ("url", "uid", "holder", "balance", "currency")
        read_only_fields = ("balance", "currency")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")


class WalletHolderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    wallet_set = WalletSerializer(many=True)

    class Meta:
        model = WalletHolder
        fields = ("user", "wallet_set")


class TransactionSerializer(serializers.ModelSerializer):
    currency = serializers.SlugRelatedField(
        queryset=Currency.objects.all(),
        slug_field='code',
    )
    receiver = serializers.SlugRelatedField(
        queryset=Wallet.objects.all(),
        slug_field='uid',
    )
    sender = serializers.SlugRelatedField(
        queryset=Wallet.objects.all(),
        slug_field='uid',
    )

    def validate(self, attrs):
        list_of_exceptions = []

        if attrs["sender"].balance < attrs["amount"]:
            list_of_exceptions.append(_("Sender wallet does not have enough money"))
        if attrs["sender"].currency != attrs["currency"]:
            list_of_exceptions.append(_("Sender wallet currency and selected currency are not equal"))
        if attrs["receiver"].currency != attrs["currency"]:
            list_of_exceptions.append(_("Receiver wallet currency and selected currency are not equal"))
        if attrs["sender"] == attrs["receiver"]:
            list_of_exceptions.append(_("You tried send money on the same wallet"))

        if list_of_exceptions:
            raise ValidationError(list_of_exceptions)

        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        sender = self.validated_data["sender"]
        receiver = self.validated_data["receiver"]
        amount = self.validated_data["amount"]

        if not Wallet.objects.filter(uid=sender.uid).filter(holder__user=user).count():
            exception_message = _("Current user doesn't have rights to this wallet. Or wallet doesn't exists")
            raise serializers.ValidationError(exception_message)
            logging.exception(exception_message)

        Wallet.objects.filter(uid=sender.uid).update(balance=F("balance") - amount)
        Wallet.objects.filter(uid=receiver.uid).update(balance=F("balance") + amount)

        return super().save(**kwargs)

    class Meta:
        model = Transaction
        fields = ("sender", "receiver", "currency", "amount")


class WalletDetailSerializer(serializers.ModelSerializer):
    holder = serializers.StringRelatedField()
    currency = serializers.SlugRelatedField(
        queryset=Currency.objects.all(),
        slug_field='code',
    )
    transactions = serializers.SerializerMethodField()

    def get_transactions(self, obj):
        incomes = Transaction.objects.filter(receiver=obj)
        expenses = Transaction.objects.filter(sender=obj)
        all_transactions = incomes | expenses
        return [TransactionSerializer(t).data for t in all_transactions]

    class Meta:
        model = Wallet
        fields = ('holder', 'currency', 'balance', 'transactions')
