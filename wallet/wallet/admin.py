from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Wallet, WalletHolder, Transaction


class TransactionSenderInline(admin.TabularInline):
    model = Transaction
    fields = ("sender", "receiver", "amount", "currency", "created")
    readonly_fields = ("sender", "receiver", "amount", "currency", "created")
    list_display = ("sender", "receiver", "amount", "currency", "created")
    fk_name = "sender"
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def sender_user(self, obj):
        return obj.sender.holder.user.username

    def receiver_user(self, obj):
        return obj.receiver.holder.user.username

    def _sender(self, obj):
        url = reverse(f"admin:wallet_wallet_change", args=[obj.sender.pk])
        return mark_safe(f"<a href='{url}'>{obj.sender}</a>")

    def _receiver(self, obj):
        url = reverse(f"admin:wallet_wallet_change", args=[obj.receiver.pk])
        return mark_safe(f"<a href='{url}'>{obj.receiver}</a>")


class TransactionReceiverInline(admin.TabularInline):
    model = Transaction
    fields = ("sender_user", "_sender", "receiver_user", "_receiver", "amount", "currency", "created")
    readonly_fields = ("sender_user", "_sender", "receiver_user", "_receiver", "amount", "currency", "created")
    fk_name = "receiver"
    extra = 0

    def sender_user(self, obj):
        return obj.sender.holder.user.username

    def receiver_user(self, obj):
        return obj.receiver.holder.user.username

    def _sender(self, obj):
        url = reverse(f"admin:wallet_wallet_change", args=[obj.sender.pk])
        return mark_safe(f"<a href='{url}'>{obj.sender}</a>")

    def _receiver(self, obj):
        url = reverse(f"admin:wallet_wallet_change", args=[obj.receiver.pk])
        return mark_safe(f"<a href='{url}'>{obj.receiver}</a>")

    def has_add_permission(self, request, obj=None):
        return False


class WalletAdmin(admin.ModelAdmin):
    inlines = [TransactionSenderInline, TransactionReceiverInline]
    list_display = ("uid", "holder", "currency", "balance")
    fields = ("holder", "currency", "balance",)


class TransactionAdmin(admin.ModelAdmin):
    fields = ("sender", "receiver", "currency", "amount", "created")
    list_display = ("sender_user", "sender", "receiver_user", "receiver", "currency", "created")
    readonly_fields = ("sender", "receiver", "amount", "currency", "created")

    def sender_user(self, obj):
        return obj.sender.holder.user.username

    def receiver_user(self, obj):
        return obj.receiver.holder.user.username

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
