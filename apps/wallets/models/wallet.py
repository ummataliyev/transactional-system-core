from django.db import models
from django.contrib.auth.models import User

from src.settings.db.postgres.mixins.timestamp import TimestampMixin


class Wallet(TimestampMixin):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name='wallet'
    )
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    class Meta:
        db_table = 'wallets'
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"Wallet {self.id} - User: {self.user.username} - Balance: {self.balance}" # noqa
