from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Wallet, WalletHolder, Transaction
from .consts import TRANSACTION_FIELDS

class TransactionSenderInline(admin.TabularInline):
    model = Transaction
    fields = TRANSACTION_FIELDS
    readonly_fields = TRANSACTION_FIELDS
    list_display = TRANSACTION_FIELDS
    fk_name = "sender"
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False


class TransactionReceiverInline(admin.TabularInline):
    model = Transaction
    fields = TRANSACTION_FIELDS
    readonly_fields = TRANSACTION_FIELDS
    fk_name = "receiver"
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False


class WalletAdmin(admin.ModelAdmin):
    inlines = [TransactionSenderInline, TransactionReceiverInline]
    list_display = ("holder", "currency", "balance")
    fields = ("holder", "currency", "balance",)


class TransactionAdmin(admin.ModelAdmin):
    fields = ("sender", "receiver", "currency", "amount")
    list_display = TRANSACTION_FIELDS
    readonly_fields = TRANSACTION_FIELDS

    def has_add_permission(self, request, obj=None):
        return False


class WalletInline(admin.TabularInline):
    model = Wallet
    fields = ("wallet_uid", "balance", "currency",)
    readonly_fields = ("wallet_uid",)
    exclude = ("uid",)
    extra = 0

    def wallet_uid(self, obj):
        url = reverse(f"admin:{obj._meta.app_label}_{obj._meta.model_name}_change", args=[obj.pk])
        return mark_safe(f"<a href='{url}'>{obj.uid}</a>")


class WalletHolderAdmin(admin.ModelAdmin):
    inlines = [WalletInline]


admin.site.register(Wallet, WalletAdmin)
admin.site.register(WalletHolder, WalletHolderAdmin)
admin.site.register(Transaction, TransactionAdmin)
