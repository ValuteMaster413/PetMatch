from typing import Iterable

from django.shortcuts import get_object_or_404

from application.common.abstractions.persistence.pet_repository import IPetRepository
from domain.shared.abstraction.value_objects.pet_uid import PetUID
from domain.shared.result import Result
from infrastructure.models import Pet


class PetRepository(IPetRepository):
    def add(self, name: str, species: str) -> Result[Pet]:
        print(name, species)

        pet = Pet.objects.create(
            _id = PetUID.create().content.value,
            name = name,
            species = species
        )

        pet.save()

        return Result.ok(pet)

    def edit(self, old_name: str, new_name: str,  new_species: str) -> Result[Pet]:
        print(old_name, new_name, new_species)
        pet = get_object_or_404(Pet, name=old_name)
        pet.name = new_name
        pet.species = new_species
        pet.save()

        return Result.ok(pet)


    def delete(self, pet_name) -> Result[None]:

        pet = get_object_or_404(Pet, name=pet_name)
        pet.delete()

        return Result.ok()

    def get_by_id(self, pet_id: str) -> Result[Pet]:
        pet = get_object_or_404(Pet, id=PetUID(pet_id))

        return Result.ok(pet)

    def get_by_name(self, pet_name: str) -> Result[Pet]:
        pet = get_object_or_404(Pet, name=pet_name)

        return Result.ok(pet)

    def list_all(self) -> Iterable[Pet]:
        pets = Pet.objects.filter()
        return pets


