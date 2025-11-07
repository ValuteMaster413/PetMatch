from django.db import transaction

from core.application.common.abstractions.persistence.abstract_unit_of_work import AbstractUnitOfWork

class DjangoUnitOfWork(AbstractUnitOfWork):
    def _execute_transaction(self) -> None:
        with transaction.atomic():
            for operation in self._operations:
                operation.operation()


