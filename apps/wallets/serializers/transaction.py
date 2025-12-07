"""
Transaction serializer
"""

from rest_framework import serializers
from apps.wallets.models.transaction import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Transaction model (transfer between wallets).

    Used to represent transactions in the API, including sender and recipient info.

    :param sender: Reference to the sender's wallet (Wallet)
    :param recipient: Reference to the recipient's wallet (Wallet)
    :param from_username: Sender's username (read-only)
    :param to_username: Recipient's username (read-only)
    :param amount: Transaction amount
    :param transaction_type: Type of transaction (e.g., transfer, bonus)
    :param status: Transaction status (read-only)
    :param transaction_group: Transaction group (read-only)
    :param description: Description or comment of the transaction
    :param created_at: Creation date and time (read-only)
    """

    from_username = serializers.CharField(
        source='sender.user.username',
        read_only=True,
        help_text="Sender's username (read-only)"
    )
    to_username = serializers.CharField(
        source='recipient.user.username',
        read_only=True,
        help_text="Recipient's username (read-only)"
    )

    class Meta:
        model = Transaction
        fields = [
            'id',
            'sender',
            'recipient',
            'from_username',
            'to_username',
            'amount',
            'transaction_type',
            'status',
            'transaction_group',
            'description',
            'created_at'
        ]
        read_only_fields = [
            'status',
            'transaction_group',
            'created_at'
        ]
        extra_kwargs = {
            'amount': {'help_text': 'Amount to transfer'},
            'transaction_type': {'help_text': 'Type of transaction'},
            'description': {'help_text': 'Transaction description'}
        }

    def create(self, validated_data):
        """
        Create a new Transaction instance.

        :param validated_data: Dictionary of validated transaction data
        :type validated_data: dict
        :return: Newly created Transaction object
        :rtype: Transaction
        """
        transaction = Transaction.objects.create(**validated_data)
        return transaction

    def update(self, instance, validated_data):
        """
        Update an existing Transaction instance.

        :param instance: Transaction object to update
        :type instance: Transaction
        :param validated_data: Dictionary of validated data for update
        :type validated_data: dict
        :return: Updated Transaction object
        :rtype: Transaction
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
