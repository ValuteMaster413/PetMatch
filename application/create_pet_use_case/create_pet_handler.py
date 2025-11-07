from core.application.common.abstractions.messaging.abstract_command_handler import AbstractCommandHandler, TCommand
from application.common.abstractions.persistence.pet_repository import IPetRepository
from application.create_pet_use_case.create_pet_command import CreatePetCommand
from domain.shared.abstraction.pet import Pet
from domain.shared.result import Result


class CreatePetHandler(AbstractCommandHandler[CreatePetCommand]):
    def __init__(self, repository: IPetRepository):
        self._repository = repository

    def handle(self, command: CreatePetCommand) -> Result[None]:

        pet = Pet(
            id=self._repository.next_id(),
            name=command.name,
            species=command.species
        )

        pet_creation_result = self._repository.add(pet)

        if pet_creation_result.failure:
            return Result.fail(pet_creation_result.error)

        return Result.ok()






