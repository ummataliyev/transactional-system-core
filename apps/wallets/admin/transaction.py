"""
UI for Transaction model
"""

from django.contrib import admin

from unfold.admin import ModelAdmin

from apps.wallets.models.transaction import Transaction


@admin.register(Transaction)
class TransactionAdmin(ModelAdmin):
    """
    Admin configuration for Transaction model.
    """
    list_display = (
        'id',
        'sender',
        'recipient',
        'amount',
        'transaction_type',
        'status',
        'transaction_group',
        'created_at'
    )
    search_fields = (
        'sender__user__username',
        'recipient__user__username',
        'transaction_group',
        'description'
    )
    list_filter = ('transaction_type', 'status', 'created_at')
    readonly_fields = ('transaction_group', 'created_at', 'updated_at')
    ordering = ('-created_at',)
