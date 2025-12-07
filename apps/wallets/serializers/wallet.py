"""
Wallet serializer
"""

from rest_framework import serializers

from apps.wallets.models.wallet import Wallet


class WalletSerializer(serializers.ModelSerializer):
    """
    Serializer for the Wallet model.

    Exposes wallet details along with the username of the associated user.

    :param id: Wallet ID
    :type id: int
    :param username: Username of the wallet owner
    :type username: str
    :param balance: Current balance of the wallet
    :type balance: Decimal
    :param created_at: Timestamp when the wallet was created
    :type created_at: datetime
    :param updated_at: Timestamp when the wallet was last updated
    :type updated_at: datetime
    """

    username = serializers.CharField(
        source='user.username',
        read_only=True,
        help_text="Username of the wallet owner"
    )

    class Meta:
        model = Wallet
        fields = [
            'id',
            'username',
            'balance',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'balance',
            'created_at',
            'updated_at'
        ]
