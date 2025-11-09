from application.delete_pet_use_case.delete_pet_command import DeletePetCommand
from application.delete_pet_use_case.delete_pet_handler import DeletePetHandler
from application.edit_pet_use_case.edit_pet_command import EditPetCommand
from application.edit_pet_use_case.edit_pet_handler import EditPetHandler
from core.application.common.abstractions.messaging.abstract_command_handler import AbstractCommandHandler
from core.infrastructure.container.container import DependencyInjectionContainer

from application.common.abstractions.persistence.pet_repository import IPetRepository
from core.infrastructure.mediator.mediator import Mediator
from domain.shared.abstraction.value_objects.pet_uid import PetUID
from infrastructure.persistence.repositories.in_memory_pet_repository import PetRepository
from application.create_pet_use_case.create_pet_command import CreatePetCommand
from application.create_pet_use_case.create_pet_handler import CreatePetHandler
from application.list_all_pets_use_case.list_all_pets_command import ListAllPetsCommand
from application.list_all_pets_use_case.list_all_pets_handler import ListAllPetsHandler
from core.application.common.abstractions.messaging.abstract_mediator import AbstractMediator

if __name__ == '__main__':
    container = DependencyInjectionContainer()
    container.add_singleton(AbstractMediator, Mediator)
    container.add_singleton(IPetRepository, PetRepository)
    container.add_transient(AbstractCommandHandler[CreatePetCommand], CreatePetHandler)
    container.add_transient(AbstractCommandHandler[ListAllPetsCommand], ListAllPetsHandler)
    container.add_transient(AbstractCommandHandler[EditPetCommand], EditPetHandler)
    container.add_transient(AbstractCommandHandler[DeletePetCommand], DeletePetHandler)

    mediator = container.get_required(AbstractMediator)

    command = CreatePetCommand(name='first_pet', species='cat')
    mediator.send(command)



    command = ListAllPetsCommand()
    mediator.send(command)



    command = CreatePetCommand(name='second_pet', species='dog')
    mediator.send(command)

    command = CreatePetCommand(name='third_pet', species='cat')
    mediator.send(command)



    command = ListAllPetsCommand()
    mediator.send(command)



    command = EditPetCommand(pet_id= input(), new_pet_name='edited_pet', new_pet_species='bird')
    mediator.send(command)

    command = ListAllPetsCommand()
    mediator.send(command)



    command = DeletePetCommand(pet_name='edited_pet')
    mediator.send(command)

    command = ListAllPetsCommand()
    mediator.send(command)

