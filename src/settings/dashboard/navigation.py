"""
Navigation settings.
Icons are: https://fonts.google.com/icons
"""

from django.urls import reverse_lazy

MAIN = {
    "title": "Main",
    "separator": True,
    "items": [
        {
            "title": "Wallet",
            "icon": "account_balance_wallet",
            "link": reverse_lazy("admin:wallets_wallet_changelist"),
        },
        {
            "title": "Transaction",
            "icon": "contactless",
            "link": reverse_lazy("admin:wallets_transaction_changelist"),
        },
    ],
}

NAVIGATION = [
    MAIN,
]
