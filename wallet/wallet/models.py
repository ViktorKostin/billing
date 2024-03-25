import logging
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Currency(models.Model):
    country = models.CharField(max_length=80, blank=False)
    # Full currency name
    currency = models.CharField(max_length=50, blank=False)
    # ISO 4217 (country currency code)
    code = models.CharField(max_length=3, blank=False)
    number = models.PositiveSmallIntegerField(blank=False)

    def __str__(self):
        return f"{self.code}"


class WalletHolder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}"


class Wallet(models.Model):
    uid = models.UUIDField(unique=True, default=uuid.uuid4)
    holder = models.ForeignKey(WalletHolder, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    balance = models.DecimalField(max_digits=6, decimal_places=2)
    transactions = models.ManyToManyField("Wallet", through="Transaction", through_fields=("sender", "receiver"))

    def __str__(self):
        return f"{self.holder.user.username} / {self.uid}"


class Transaction(models.Model):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(Wallet, related_name="transaction_sender", on_delete=models.DO_NOTHING)
    receiver = models.ForeignKey(
        Wallet,
        related_name="transaction_receiver",
        on_delete=models.DO_NOTHING,
    )
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    created = models.DateTimeField(default=timezone.localtime)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return f"transcaction: {self.uid}"

    def clean(self):
        list_of_exceptions = []

        if self.sender.balance < self.amount:
            list_of_exceptions.append(_("Sender wallet does not have enough money"))
        if self.sender.currency != self.currency:
            list_of_exceptions.append(_("Sender wallet currency and selected currency are not equal"))
        if self.receiver.currency != self.currency:
            list_of_exceptions.append(_("Receiver wallet currency and selected currency are not equal"))
        if self.sender == self.receiver:
            list_of_exceptions.append(_("You tried send money on the same wallet"))

        if list_of_exceptions:
            logging.exception(list_of_exceptions)
            raise ValidationError(list_of_exceptions)



