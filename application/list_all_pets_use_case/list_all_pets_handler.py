from typing import List, Iterable
from core.application.common.abstractions.messaging.abstract_command_handler import AbstractCommandHandler, TCommand
from application.common.abstractions.persistence.pet_repository import IPetRepository
from application.list_all_pets_use_case.list_all_pets_command import ListAllPetsCommand
from domain.shared.abstraction.pet import Pet
from domain.shared.result import Result


class ListAllPetsHandler(AbstractCommandHandler[ListAllPetsCommand]):
    def __init__(self, repository: IPetRepository):
        self._repository = repository

    def handle(self, command: ListAllPetsCommand) -> Result[Iterable[Pet]]:
        all_pets = self._repository.list_all()

        print(all_pets)

        return Result.ok(
            all_pets
        )






