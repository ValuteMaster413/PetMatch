from core.application.common.abstractions.messaging.abstract_command_handler import AbstractCommandHandler
from core.infrastructure.container.container import DependencyInjectionContainer

from application.common.abstractions.persistence.pet_repository import IPetRepository
from core.infrastructure.mediator.mediator import Mediator
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

    command = CreatePetCommand(name='first_pet', species='cat')

    mediator = container.get_required(AbstractMediator)

    mediator.send(command)

    command = ListAllPetsCommand()

    mediator = container.get_required(AbstractMediator)

    mediator.send(command)

    command = CreatePetCommand(name='second_pet', species='dog')

    mediator = container.get_required(AbstractMediator)

    mediator.send(command)

    command = ListAllPetsCommand()

    mediator = container.get_required(AbstractMediator)

    mediator.send(command)
