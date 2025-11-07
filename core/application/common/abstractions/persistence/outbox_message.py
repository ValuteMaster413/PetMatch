from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from core.application.common.abstractions.persistence.outbox_message_uid import OutboxMessageUID

@dataclass
class OutboxMessage:
    uid: OutboxMessageUID
    occurred_at: datetime
    content: str
    type: str
    handled_at: Optional[datetime] = None
    error: Optional[str] = None



