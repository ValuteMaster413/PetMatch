from application.common.abstractions.persistence.pet_repository import IPetRepository
from application.delete_pet_use_case.delete_pet_command import DeletePetCommand
from core.application.common.abstractions.messaging.abstract_command_handler import AbstractCommandHandler
from domain.shared.result import Result



class DeletePetHandler(AbstractCommandHandler):
    def __init__(self, repository: IPetRepository):
        self._repository = repository


    def handle(self, command: DeletePetCommand) -> Result[None]:
        pet_deletion_result = self._repository.delete(command.pet_name)

        if pet_deletion_result.failure:
            return Result.fail(pet_deletion_result.error)

        return Result.ok(None)
