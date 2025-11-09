from typing import Iterable

from application.common.abstractions.persistence.pet_repository import IPetRepository
from domain.shared.abstraction.pet import Pet

from core.domain.shared.result import Result
from typing import Dict

from domain.shared.abstraction.value_objects.pet_uid import PetUID


class PetRepository(IPetRepository):
    def __init__(self):
        self._storage: Dict[PetUID, Pet] = {}

    def add(self, name: str, species: str) -> Result[None]:

        pet = Pet(
            id = PetUID.create().content,
            name = name,
            species = species
        )

        pet_id = pet.id

        self._storage[pet_id] = pet

        return Result.ok(None)

    def edit(self, pet_id: PetUID, new_pet_name: str, new_pet_species: str) -> Result[Pet]:
        pet = self._storage.get(pet_id)

        pet.name = new_pet_name
        pet.species = new_pet_species

        self._storage[pet_id] = pet

        return Result.ok(pet)

    def delete(self, pet_name: str) -> Result[None]:
        for pid, pet in list(self._storage.items()):
            if pet.name == pet_name:
                del self._storage[pid]

        return Result.ok(None)

    def get_by_id(self, pet_id: PetUID) -> Result[Pet]:
        pet = self._storage[pet_id]

        return Result.ok(pet)

    def get_by_name(self, pet_name: str) -> Result[Pet]:
        result_pet: Pet = None

        for pet in self._storage.values():
            if pet.name == pet_name:
                result_pet = pet

        return Result.ok(result_pet)


    def list_all(self) -> Iterable[Pet]:
        return list(self._storage.values())
