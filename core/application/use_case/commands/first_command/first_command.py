from dataclasses import dataclass

from core.application.common.abstractions.messaging.abstract_command import AbstractCommand


@dataclass
class FirstCommand(AbstractCommand):
    user_id: int
    action_name: str