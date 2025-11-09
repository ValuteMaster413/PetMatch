from __future__ import annotations
from typing import Iterable, Optional
from abc import ABC
from domain.shared.abstraction.pet import Pet
from domain.shared.abstraction.value_objects.pet_uid import PetUID


class IPetRepository(ABC):
    def add(self, name: str, species) -> None:
        ...

    def edit(self, pet_id: PetUID, new_pet_name: str, new_pet_species: str) -> Optional[Pet]:
        ...

    def delete(self,  pet_name: str) -> Optional[Pet]:
        ...

    def get_by_id(self, pet_id: PetUID) -> Optional[Pet]:
        ...

    def get_by_name(self, pet_name: str) -> Optional[Pet]:
        ...

    def list_all(self) -> Iterable[Pet]:
        ...
