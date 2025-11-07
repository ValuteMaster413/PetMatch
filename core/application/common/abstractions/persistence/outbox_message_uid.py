import uuid
from dataclasses import dataclass

@dataclass(frozen=True)
class OutboxMessageUID:
    value: str

    @classmethod
    def new(cls) -> 'OutboxMessageUID':
        return OutboxMessageUID(value=uuid.uuid4().hex)
