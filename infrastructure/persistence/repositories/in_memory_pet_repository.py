import uuid
from typing import Dict, Iterable
from uuid import UUID

from application.common.abstractions.persistence.pet_repository import IPetRepository
from domain.shared.abstraction.pet import Pet

from core.domain.shared.result import Result
from typing import Dict


class PetRepository(IPetRepository):
    def __init__(self):
        self._storage: Dict[str, Pet] = {}

    def add(self, pet: Pet) -> Result[None]:
        pet_id = str(pet.id)
        self._storage[pet_id] = pet

        return Result.ok(None)

    def get_by_id(self, pet_id: UUID) -> Result[Pet]:
        pass

    def list_all(self) -> Iterable[Pet]:
        return list(self._storage.values())

    def next_id(self) -> UUID:
        next_id = uuid.uuid4()
        return next_id