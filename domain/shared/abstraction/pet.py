from __future__ import annotations
from dataclasses import dataclass
from uuid import UUID, uuid4

from core.domain.contexts.action_context.aggregates.action.value_objects.action_uid import ActionUID


@dataclass
class Pet:
    id: ActionUID
    name: str
    species: str

