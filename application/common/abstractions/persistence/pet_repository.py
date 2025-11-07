from __future__ import annotations
from typing import Iterable, Optional
from abc import ABC
from uuid import UUID
from domain.shared.abstraction.pet import Pet

class IPetRepository(ABC):
    def add(self, pet: Pet) -> None:
        ...

    def get_by_id(self, pet_id: UUID) -> Optional[Pet]:
        ...

    def list_all(self) -> Iterable[Pet]:
        ...

    def next_id(self) -> UUID:
        ...