from django.urls import path
from apps.wallets.views.wallet import WalletDetailAPIView
from apps.wallets.views.wallet import WalletListCreateAPIView
from apps.wallets.views.transfer import TransferAPIView
from apps.wallets.views.transcation import TransactionHistoryAPIView


urlpatterns = [
    path(
        'wallets/',
        WalletListCreateAPIView.as_view(),
        name='wallet-list-create'
    ),
    path(
        'wallets/<int:wallet_id>/',
        WalletDetailAPIView.as_view(),
        name='wallet-detail'
    ),
    path(
        'transfer/',
        TransferAPIView.as_view(),
        name='transfer'
    ),
    path(
        'transactions/',
        TransactionHistoryAPIView.as_view(),
        name='transaction-history'
    ),
]
