from core.application.common.abstractions.di_container.abstract_di_container import AbstractDIContainer
from core.application.common.abstractions.messaging.abstract_event_handler import AbstractEventHandler
from core.application.common.abstractions.messaging.abstract_query_response import AbstractQueryResponse
from core.application.common.abstractions.persistence.transactional_operation import TransactionalOperation
from core.application.common.abstractions.messaging.abstract_command_handler import AbstractCommandHandler
from core.application.common.abstractions.messaging.abstract_command import AbstractCommand
from core.application.common.abstractions.messaging.abstract_query import AbstractQuery
from core.application.common.abstractions.messaging.abstract_query_handler import AbstractQueryHandler
from core.application.common.abstractions.messaging.abstract_mediator import AbstractMediator
from typing import Dict, Type, Union, TypeVar

from core.domain.shared.abstractions.domain_event import DomainEvent
from core.domain.shared.result import Result

T = TypeVar('T', bound=Union[AbstractQueryResponse, TransactionalOperation])

class Mediator(AbstractMediator):
    def __init__(self, di_container: AbstractDIContainer):
        self._command_handlers: Dict[Type[AbstractCommand], AbstractCommandHandler] = {}
        self._query_handlers: Dict[Type[AbstractQuery], AbstractQueryHandler] = {}
        self._event_handlers: Dict[Type[DomainEvent], AbstractEventHandler] = {}
        self._container = di_container

    def send(self, request: Union[AbstractCommand, AbstractQuery, DomainEvent]) -> Result[T]:
        if isinstance(request, AbstractCommand):
            return self._dispatch_command(request)

        elif isinstance(request, AbstractQuery):
            return self._dispatch_query(request)

        elif isinstance(request, DomainEvent):
            return self._dispatch_event(request)
        else:
            raise ValueError("Unsupported request type")

    def _dispatch_event(self, event: DomainEvent) -> Result[TransactionalOperation]:
        event_handler = self._event_handlers.get(type(event))
        if event_handler is None:
            handler_instance = self._container.get_required(AbstractEventHandler[type(event)])
            if self._container.is_singleton_implementation(AbstractEventHandler[type(event)]):
                self._event_handlers[type(event)] = handler_instance
            return handler_instance.handle(event)
        return event_handler.handle(event)

    def _dispatch_command(self, command: AbstractCommand) -> Result:
        command_handler = self._command_handlers.get(type(command))
        if command_handler is None:
            handler_instance = self._container.get_required(AbstractCommandHandler[type(command)])
            if self._container.is_singleton_implementation(AbstractCommandHandler[type(command)]):
                self._command_handlers[type(command)] = handler_instance
            return handler_instance.handle(command)
        return command_handler.handle(command)

    def _dispatch_query(self, query: AbstractQuery) -> Result[AbstractQueryResponse]:
        # type(query).__orig_bases__[0].__args__[0] <---- TO GET GENERIC TYPES
        query_handler = self._query_handlers.get(type(query))
        if query_handler is None:
            handler_instance = self._container.get_required(AbstractQueryHandler[type(query)])
            if self._container.is_singleton_implementation(AbstractQueryHandler[type(query)]):
                self._query_handlers[type(query)] = handler_instance
            return handler_instance.handle(query)
        return query_handler.handle(query)


