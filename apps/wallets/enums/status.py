from enum import Enum


class Status(Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'

    @property
    def label(self):
        return self.name.title()
