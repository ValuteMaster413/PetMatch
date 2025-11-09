from application.edit_pet_use_case.edit_pet_command import EditPetCommand
from core.application.common.abstractions.messaging.abstract_command_handler import AbstractCommandHandler
from application.common.abstractions.persistence.pet_repository import IPetRepository
from domain.shared.abstraction.value_objects.pet_uid import PetUID
from domain.shared.result import Result


class EditPetHandler(AbstractCommandHandler[EditPetCommand]):
    def __init__(self, repository: IPetRepository):
        self._repository = repository

    def handle(self, command: EditPetCommand) -> Result[None]:
        pet_id = PetUID.create(command.pet_id).content
        pet_edition_result = self._repository.edit(pet_id, command.new_pet_name, command.new_pet_species)

        if pet_edition_result.failure:
            return Result.fail(pet_edition_result.error)

        return Result.ok(None)






