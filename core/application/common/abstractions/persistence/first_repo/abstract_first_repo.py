from abc import abstractmethod

from core.application.common.abstractions.persistence.abstract_repository import AbstractRepository
from core.domain.contexts.action_context.aggregates.action.action import Action
from core.domain.shared.result import Result


class IFirstRepository(AbstractRepository):
    @abstractmethod
    def get_action_by_name(self, name: str) -> Result[Action]:
        ...

    @abstractmethod
    def save(self, action: Action) -> Result[None]:
        ...