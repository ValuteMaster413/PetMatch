from core.application.common.abstractions.persistence.first_repo.abstract_first_repo import IFirstRepository
from core.domain.contexts.action_context.aggregates.action.action import Action
from core.domain.contexts.action_context.aggregates.action.value_objects.action_uid import ActionUID
from core.domain.shared.result import Result


class FirstRepository(IFirstRepository):
    def get_action_by_name(self, name: str) -> Result[Action]:
        return Result.ok(
            Action(
                _id=ActionUID.create().content,
                _name = 'Some name'
            )
        )

    def save(self, action: Action) -> Result[None]:
        print(action)
        return Result.ok(None)