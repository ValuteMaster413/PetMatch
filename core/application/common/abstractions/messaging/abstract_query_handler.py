from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from core.application.common.abstractions.messaging.abstract_query import AbstractQuery
from core.application.common.abstractions.messaging.abstract_query_response import AbstractQueryResponse
from core.domain.shared.result import Result

TQuery = TypeVar('TQuery', bound=AbstractQuery)

class AbstractQueryHandler(Generic[TQuery], ABC):
    @abstractmethod
    def handle(self, query: TQuery) -> Result[AbstractQueryResponse]:
        ...