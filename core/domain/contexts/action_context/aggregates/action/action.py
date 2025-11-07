from dataclasses import dataclass

from core.domain.contexts.action_context.aggregates.action.value_objects.action_uid import ActionUID
from core.domain.shared.abstractions.entity import Entity

@dataclass
class Action(Entity[ActionUID]):
    _name: str

    @property
    def name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name