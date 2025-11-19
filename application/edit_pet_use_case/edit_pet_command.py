from dataclasses import dataclass

from core.application.common.abstractions.messaging.abstract_command import AbstractCommand
from domain.shared.abstraction.value_objects.pet_uid import PetUID


@dataclass
class EditPetCommand(AbstractCommand):
    old_pet_name: str
    new_pet_name: str
    new_pet_species: str

