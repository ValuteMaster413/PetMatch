from dataclasses import dataclass
from typing import Callable, Union, List, Optional

from core.application.common.abstractions.persistence.outbox_message import OutboxMessage
from core.domain.shared.abstractions.entity import Entity


@dataclass
class TransactionalOperation:
    operation: Callable
    aggregate: Optional[Union[Entity, List[Entity], List[OutboxMessage]]]