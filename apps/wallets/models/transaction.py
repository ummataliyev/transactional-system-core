import uuid

from django.db import models

from apps.wallets.models.wallet import Wallet

from apps.wallets.enums.status import Status
from apps.wallets.enums.transaction import TransactionType

from src.settings.db.postgres.mixins.timestamp import TimestampMixin


class Transaction(TimestampMixin):
    sender = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name='outgoing_transactions',
        null=True,
        blank=True
    )
    recipient = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name='incoming_transactions'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(
        max_length=20,
        choices=[(tag.value, tag.label) for tag in TransactionType],
        default=TransactionType.TRANSFER.value
    )
    status = models.CharField(
        max_length=20,
        choices=[(tag.value, tag.label) for tag in Status],
        default=Status.PENDING.value
    )
    transaction_group = models.UUIDField(default=uuid.uuid4, editable=False)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'transactions'
        indexes = [
            models.Index(fields=['sender', 'created_at']),
            models.Index(fields=['recipient', 'created_at']),
            models.Index(fields=['transaction_group']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Transaction {self.id} - {self.amount} from {self.sender_id} to {self.recipient_id}" # noqa
