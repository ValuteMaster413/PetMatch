from dataclasses import dataclass, field
from typing import TypeVar, Generic, List

from core.domain.shared.abstractions.domain_event import DomainEvent

T = TypeVar('T')

@dataclass
class Entity(Generic[T]):
    _id: T
    _domain_events: List[DomainEvent] = field(init=False)

    def __post_init__(self):
        self._domain_events = []

    @property
    def uid(self) -> T:
        return self._id

    @property
    def str_uid(self) -> str:
        return self._id.value

    @property
    def domain_events(self) -> List[DomainEvent]:
        return self._domain_events

    def raise_domain_event(self, event: DomainEvent) -> None:
        self._domain_events.append(event)

    def clear_events(self) -> None:
        self._domain_events = []

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return getattr(self, 'uid', None) == getattr(other, 'uid', None)
        return False

