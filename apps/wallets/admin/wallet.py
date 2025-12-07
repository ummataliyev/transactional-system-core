"""
UI for Wallet model
"""

from django.contrib import admin

from unfold.admin import ModelAdmin

from apps.wallets.models.wallet import Wallet


@admin.register(Wallet)
class WalletAdmin(ModelAdmin):
    """
    Admin configuration for Wallet model.
    """
    list_display = ('id', 'user', 'balance', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('created_at',)
    ordering = ('id',)
