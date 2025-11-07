import uuid
from typing import Dict, Iterable
from uuid import UUID

from application.common.abstractions.persistence.pet_repository import IPetRepository
from core.domain.contexts.action_context.aggregates.action.value_objects.action_uid import ActionUID
from domain.shared.abstraction.pet import Pet

from core.domain.shared.result import Result
from typing import Dict


class PetRepository(IPetRepository):
    def __init__(self):
        self._storage: Dict[ActionUID, Pet] = {}

    def add(self, name: str, species: str) -> Result[None]:

        pet = Pet(
            id = ActionUID.create().content,
            name = name,
            species = species
        )

        pet_id = pet.id

        self._storage[pet_id] = pet

        return Result.ok(None)

    def get_by_id(self, pet_id: UUID) -> Result[Pet]:
        pass

    def list_all(self) -> Iterable[Pet]:
        return list(self._storage.values())
