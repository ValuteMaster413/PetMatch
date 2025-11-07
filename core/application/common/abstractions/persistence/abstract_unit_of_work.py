import json
import traceback
from abc import ABC, abstractmethod
from dataclasses import asdict
from datetime import datetime
from typing import List

from core.application.common.abstractions.messaging.abstract_mediator import AbstractMediator
from core.application.common.abstractions.persistence.outbox_message import OutboxMessage
from core.application.common.abstractions.persistence.outbox_message_uid import OutboxMessageUID
from core.application.common.errors.persistence_errors import PersistenceErrors
from core.application.common.abstractions.persistence.repositories.outbox_messages import IOutboxMessagesRepository
from core.application.common.abstractions.persistence.transactional_operation import TransactionalOperation
from core.domain.shared.abstractions.domain_event import DomainEvent
from core.application.common.abstractions.persistence.utils.date_enums_json_encoder import WithDatesEnumsEncoder
from core.domain.shared.result import Result


class AbstractUnitOfWork(ABC):
    def __init__(self, mediator: AbstractMediator, outbox_messages_repository: IOutboxMessagesRepository):
        self._operations: List[TransactionalOperation] = []
        self._transactional_events: List[DomainEvent] = []
        self._background_events: List[DomainEvent] = []
        self._mediator = mediator
        self._outbox_messages_repo = outbox_messages_repository

    @abstractmethod
    def _execute_transaction(self) -> None:
        ...

    def create_transaction(self, operations: List[TransactionalOperation]) -> None:
        self._operations = operations

    def commit(self) -> Result[None]:
        """
        Method to execute all ORM operations_TO_DELETE as a single transaction. Steps:
            - Extract events from aggregates involved into transaction and sort into Transactional Events and Background Events
            - Handle Transactional Events one by one via UoW Mediator and store results into self._operations
            - Convert Background events into Outbox messages and add into current transaction
            - Try to execute transaction
            - Return Persistence error if failed
        """

        self._extract_domain_event()
        result = self._add_transactional_events_to_current_transaction()
        if result.failure:
            return Result.fail(result.error)
        self._convert_background_events_into_outbox_messages()

        try:
            self._execute_transaction()
            return Result.ok()
        except Exception as e:
            return PersistenceErrors.UnitOfWork.failure(e, traceback.format_exc())

    def _convert_background_events_into_outbox_messages(self) -> None:
        messages = []
        for event in self._background_events:
            event_dict = asdict(event)
            messages.append(OutboxMessage(
                uid=OutboxMessageUID.new(),
                occurred_at=datetime.now(),
                content=json.dumps(event_dict, cls=WithDatesEnumsEncoder),
                type=event.__class__.__module__ + '.' + event.__class__.__name__
            ))
        if len(messages) != 0:
            self._operations.append(self._outbox_messages_repo.save_bulk(messages))

    def _add_transactional_events_to_current_transaction(self) -> Result:
        for event in self._transactional_events:
            event_handling_transactional_operation_to_execute_result = self._mediator.send(event)
            if event_handling_transactional_operation_to_execute_result.failure:
                return Result.fail(event_handling_transactional_operation_to_execute_result.error)
            if event_handling_transactional_operation_to_execute_result.content is not None:
                self._operations.append(event_handling_transactional_operation_to_execute_result.content)
        return Result.ok()

    def _extract_domain_event(self) -> None:
        for operation in self._operations:
            if operation.aggregate is not None:
                aggregate = operation.aggregate
                # Exclude bulk_operations for now.
                if type(aggregate)!= list and type(aggregate)!= tuple:
                    events = aggregate.domain_events
                    for event in events:
                        if event.purpose == DomainEvent.Purpose.Transactional:
                            self._transactional_events.append(event)

                        if event.purpose == DomainEvent.Purpose.Background:
                            self._background_events.append(event)

                    aggregate.clear_events()