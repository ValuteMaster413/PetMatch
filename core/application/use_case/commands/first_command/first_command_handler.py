from core.application.common.abstractions.messaging.abstract_command_handler import AbstractCommandHandler
from core.application.common.abstractions.persistence.first_repo.abstract_first_repo import IFirstRepository
from core.application.use_case.commands.first_command.first_command import FirstCommand
from core.domain.contexts.action_context.aggregates.action.action import Action
from core.domain.shared.result import Result


class FirstCommandHandler(AbstractCommandHandler[FirstCommand]):
    def __init__(self, repository: IFirstRepository):
        self._repository = repository

    def handle(self, command: FirstCommand) -> Result[None]:
        action_result = self._repository.get_action_by_name(command.action_name)
        if action_result.failure:
            return Result.fail(action_result.error)

        action: Action = action_result.content

        action.set_name("New action")

        save_result = self._repository.save(action)

        if save_result.failure:
            return Result.fail(save_result.error)

        return Result.ok()
