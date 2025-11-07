from abc import ABC, abstractmethod
from typing import TypeVar, Union

from core.application.common.abstractions.messaging.abstract_query_response import AbstractQueryResponse
from core.application.common.abstractions.messaging.abstract_query import AbstractQuery
from core.application.common.abstractions.messaging.abstract_command import AbstractCommand
from core.application.common.abstractions.persistence.transactional_operation import TransactionalOperation
from core.domain.shared.abstractions.domain_event import DomainEvent
from core.domain.shared.result import Result

T = TypeVar('T', bound=Union[AbstractQueryResponse, TransactionalOperation, None])

class AbstractMediator(ABC):
    @abstractmethod
    def send(self, request: Union[AbstractCommand, AbstractQuery, DomainEvent]) -> Result[T]:
        ...

