from dataclasses import dataclass
from uuid import UUID

from core.application.common.abstractions.messaging.abstract_command import AbstractCommand


@dataclass
class CreatePetCommand(AbstractCommand):
    name: str
    species: str

