from __future__ import annotations
from dataclasses import dataclass

from domain.shared.abstraction.value_objects.pet_uid import PetUID


@dataclass
class Pet:
    id: PetUID
    name: str
    species: str

