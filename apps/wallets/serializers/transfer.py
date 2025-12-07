"""
Transfer serializer
"""

from decimal import Decimal

from rest_framework import serializers

from apps.wallets.models.wallet import Wallet


class TransferSerializer(serializers.Serializer):
    """
    Serializer for transferring funds between wallets.

    Validates that the sender and recipient wallets exist, the amount is positive,
    and that the transfer is not to the same wallet.

    :param sender_id: ID of the sender's wallet
    :type sender_id: int
    :param recipient_id: ID of the recipient's wallet
    :type recipient_id: int
    :param amount: Amount to transfer
    :type amount: Decimal
    :param description: Optional description of the transfer
    :type description: str
    """

    sender_id = serializers.IntegerField(required=True, help_text="ID of the sender's wallet")
    recipient_id = serializers.IntegerField(required=True, help_text="ID of the recipient's wallet")
    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=True,
        help_text="Amount to transfer (must be greater than 0)"
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
        help_text="Optional transfer description"
    )

    def validate_amount(self, value):
        """
        Validate that the transfer amount is greater than zero.

        :param value: The amount to validate
        :type value: Decimal
        :return: The validated amount
        :rtype: Decimal
        :raises serializers.ValidationError: If the amount is less than or equal to zero
        """
        if value <= Decimal('0'):
            raise serializers.ValidationError("Amount must be greater than 0")
        return value

    def validate(self, data):
        """
        Validate that sender and recipient are different and both wallets exist.

        :param data: Dictionary containing sender_id, recipient_id, and amount
        :type data: dict
        :return: Validated data
        :rtype: dict
        :raises serializers.ValidationError: If sender == recipient or wallets don't exist
        """
        if data['sender_id'] == data['recipient_id']:
            raise serializers.ValidationError("Cannot transfer to the same wallet")

        try:
            Wallet.objects.get(id=data['sender_id'])
        except Wallet.DoesNotExist:
            raise serializers.ValidationError("Source wallet does not exist")

        try:
            Wallet.objects.get(id=data['recipient_id'])
        except Wallet.DoesNotExist:
            raise serializers.ValidationError("Destination wallet does not exist")

        return data
