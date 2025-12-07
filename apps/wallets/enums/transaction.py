from enum import Enum


class TransactionType(Enum):
    TRANSFER = 'transfer'
    COMMISSION = 'commission'

    @property
    def label(self):
        return self.name.title()
