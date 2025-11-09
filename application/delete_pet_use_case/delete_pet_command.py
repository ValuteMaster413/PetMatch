from dataclasses import dataclass

from core.application.common.abstractions.messaging.abstract_command import AbstractCommand


@dataclass
class DeletePetCommand(AbstractCommand):
    pet_name: str
