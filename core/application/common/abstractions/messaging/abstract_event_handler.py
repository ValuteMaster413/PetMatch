from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from core.application.common.abstractions.persistence.transactional_operation import TransactionalOperation
from core.domain.shared.abstractions.domain_event import DomainEvent
from core.domain.shared.result import Result

T = TypeVar('T', bound=DomainEvent)

class AbstractEventHandler(Generic[T], ABC):
    @abstractmethod
    def handle(self, event: T) -> Result[TransactionalOperation]:
        ...