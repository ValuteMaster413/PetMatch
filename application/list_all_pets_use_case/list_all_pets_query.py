from dataclasses import dataclass
from uuid import UUID

from core.application.common.abstractions.messaging.abstract_command import AbstractCommand
from core.application.common.abstractions.messaging.abstract_query import AbstractQuery


@dataclass
class ListAllPetsQuery(AbstractQuery):
    pass