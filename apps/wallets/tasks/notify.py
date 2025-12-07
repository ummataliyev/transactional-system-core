"""
Background task for Transactions
"""

import time
import random

from celery import shared_task

from src.settings.utils.logging import logger


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=3
)
def send_notification(self, recipient_id, amount, sender_id, transaction_group_id):
    """
    Asynchronous task to send a transfer notification.

    Simulates a long request (e.g., Telegram API) and retries on failure.

    :param self: Task instance (bind=True)
    :param recipient_id: ID of the recipient wallet
    :type recipient_id: int
    :param amount: Amount transferred
    :type amount: Decimal
    :param sender_id: ID of the sender wallet
    :type sender_id: int
    :param transaction_group_id: UUID of the transaction group
    :type transaction_group_id: str
    :return: Dictionary with task status and details
    :rtype: dict
    """
    try:
        logger.info(
            f"[Attempt {self.request.retries + 1}/4] Sending notification to wallet {recipient_id}"
        )

        logger.info("Simulating long request (5 seconds)...")
        time.sleep(5)

        if random.random() < 0.3:
            logger.warning("Simulated network error occurred")
            raise Exception("Simulated network error: Failed to connect to notification service")

        logger.info(
            f"✓ Notification sent successfully to wallet {recipient_id}. "
            f"Amount: {amount}, Transaction group: {transaction_group_id}"
        )

        return {
            'status': 'success',
            'recipient_id': recipient_id,
            'amount': str(amount),
            'transaction_group_id': transaction_group_id
        }

    except Exception as exc:
        logger.error(
            f"✗ Error sending notification (attempt {self.request.retries + 1}/4): {str(exc)}"
        )

        if self.request.retries < self.max_retries:
            logger.info(f"Retrying in 3 seconds... (attempt {self.request.retries + 2}/4)")
            raise self.retry(exc=exc, countdown=3)
        else:
            logger.error(
                f"✗ All retry attempts exhausted for wallet {recipient_id}. "
                f"Manual intervention required."
            )
            return {
                'status': 'failed',
                'error': str(exc),
                'retries_exhausted': True
            }


@shared_task
def cleanup_old_transactions():
    """
    Periodic task to clean up old completed transactions (e.g., older than 90 days).

    :return: Dictionary containing the number of deleted transactions
    :rtype: dict
    """
    from datetime import timedelta
    from django.utils import timezone
    from apps.wallets.models.transaction import Transaction

    threshold_date = timezone.now() - timedelta(days=90)
    deleted_count = Transaction.objects.filter(
        created_at__lt=threshold_date,
        status='completed'
    ).delete()[0]

    logger.info(f"Cleaned up {deleted_count} old transactions")
    return {'deleted_count': deleted_count}
