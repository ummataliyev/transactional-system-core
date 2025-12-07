"""
Transfer service
"""

import uuid

from decimal import Decimal

from django.db.models import F
from django.db import transaction

from apps.wallets.models.wallet import Wallet
from apps.wallets.models.transaction import Transaction
from apps.wallets.tasks.notify import send_notification

from src.settings.utils.logging import logger


class TransferService:
    """
    Handles wallet-to-wallet transfers with optional commission and async notifications.

    Features:
        - Atomic transactions with race condition protection.
        - Commission applied for large transfers.
        - Async notification sent after successful transfer.
    """

    COMMISSION_THRESHOLD = Decimal('1000.00')
    COMMISSION_RATE = Decimal('0.10')  # 10%
    ADMIN_WALLET_ID = 1

    @classmethod
    def execute_transfer(
        cls,
        sender_id: int,
        recipient_id: int,
        amount: Decimal,
        description: str = ''
    ) -> dict:

        """
        Perform an atomic wallet-to-wallet transfer with optional commission.

        Prevents double-spending using `select_for_update` and schedules an async notification.

        :param sender_id: ID of the sending wallet
        :param recipient_id: ID of the receiving wallet
        :param amount: Amount to transfer
        :param description: Optional transaction description
        :raises ValueError: If wallets not found or insufficient funds
        :return: Transfer details including transaction ID, group, amount, commission, and total debited
        :rtype: dict
        """

        with transaction.atomic():
            wallet_ids = sorted([sender_id, recipient_id, cls.ADMIN_WALLET_ID])
            locked_wallets = {
                w.id: w for w in Wallet.objects.select_for_update().filter(id__in=wallet_ids) # noqa
            }

            sender = locked_wallets.get(sender_id)
            recipient = locked_wallets.get(recipient_id)

            if not sender or not recipient:
                raise ValueError("Wallet not found")

            if sender.balance < amount:
                raise ValueError(f"Insufficient funds. Available: {sender.balance}, Required: {amount}")

            commission_amount = Decimal('0')
            if amount > cls.COMMISSION_THRESHOLD:
                commission_amount = amount * cls.COMMISSION_RATE

            total_debit = amount + commission_amount

            if sender.balance < total_debit:
                raise ValueError(
                    f"Insufficient funds including commission. Available: {sender.balance}, Required: {total_debit}" # noqa
                )

            transaction_group_id = uuid.uuid4()

            Wallet.objects.filter(id=sender_id).update(balance=F('balance') - total_debit) # noqa
            Wallet.objects.filter(id=recipient_id).update(balance=F('balance') + amount) # noqa

            main_transaction = Transaction.objects.create(
                sender_id=sender_id,
                recipient_id=recipient_id,
                amount=amount,
                transaction_type='transfer',
                status='completed',
                transaction_group=transaction_group_id,
                description=description
            )

            if commission_amount > 0:
                admin_wallet = locked_wallets.get(cls.ADMIN_WALLET_ID)
                if admin_wallet:
                    Wallet.objects.filter(id=cls.ADMIN_WALLET_ID).update(
                        balance=F('balance') + commission_amount
                    )

                    Transaction.objects.create(
                        sender_id=sender_id,
                        recipient_id=cls.ADMIN_WALLET_ID,
                        amount=commission_amount,
                        transaction_type='commission',
                        status='completed',
                        transaction_group=transaction_group_id,
                        description=f'Commission for transfer {transaction_group_id}' # noqa
                    )

            logger.info(
                f"Transfer completed: {amount} from wallet {sender_id} "
                f"to wallet {recipient_id}, commission: {commission_amount}"
            )

            transaction.on_commit(
                lambda: send_notification.delay(
                    recipient_id,
                    amount,
                    sender_id,
                    str(transaction_group_id)
                )
            )

            return {
                'success': True,
                'transaction_id': main_transaction.id,
                'transaction_group': str(transaction_group_id),
                'amount': str(amount),
                'commission': str(commission_amount),
                'total_debited': str(total_debit)
            }
