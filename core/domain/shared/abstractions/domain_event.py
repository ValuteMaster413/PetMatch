from dataclasses import dataclass
from abc import ABC
from enum import Enum

# class EventPurpose(Enum):
#     Transactional = 'Transactional'
#     Background = 'Background'

@dataclass(frozen=True)
class DomainEvent(ABC):
    purpose: 'Purpose'

    class Purpose(Enum):
        Transactional = 'Transactional'
        Background = 'Background'



