from __future__ import annotations
from dataclasses import dataclass
from uuid import UUID, uuid4

@dataclass
class Pet:
    id: UUID
    name: str
    species: str

    @staticmethod
    def create(name: str, species: str) -> Pet:
        name = name.strip()
        species = species.strip()

        if not name:
            raise ValueError("Pet name cannot be empty.")
        if not species:
            raise ValueError("Pet species cannot be empty.")

        return Pet(id=uuid4(), name=name, species=species)
