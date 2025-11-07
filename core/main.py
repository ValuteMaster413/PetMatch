from core.application.common.abstractions.messaging.abstract_command_handler import AbstractCommandHandler
from core.application.common.abstractions.messaging.abstract_mediator import AbstractMediator
from core.application.common.abstractions.persistence.first_repo.abstract_first_repo import IFirstRepository
from core.application.use_case.commands.first_command.first_command import FirstCommand
from core.application.use_case.commands.first_command.first_command_handler import FirstCommandHandler
from core.infrastructure.container.container import DependencyInjectionContainer
from core.infrastructure.mediator.mediator import Mediator
from core.infrastructure.persistence.repositories.action_repository import FirstRepository

if __name__ == '__main__':
    container = DependencyInjectionContainer()
    container.add_singleton(AbstractMediator, Mediator)
    container.add_transient(IFirstRepository, FirstRepository)
    container.add_transient(AbstractCommandHandler[FirstCommand], FirstCommandHandler)

    command = FirstCommand(user_id=1, action_name="New name")

    mediator = container.get_required(AbstractMediator)

    mediator.send(command)

