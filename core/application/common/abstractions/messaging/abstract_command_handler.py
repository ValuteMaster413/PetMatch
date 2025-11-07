from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from core.application.common.abstractions.messaging.abstract_command import AbstractCommand
from core.domain.shared.result import Result

TCommand = TypeVar('TCommand', bound=AbstractCommand)

class AbstractCommandHandler(Generic[TCommand], ABC):
    @abstractmethod
    def handle(self, command: TCommand) -> Result:
        ...
