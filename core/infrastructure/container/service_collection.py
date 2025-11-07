from typing import List, Type, Optional, TypeVar

from core.infrastructure.container.service_scope import ServiceScope
from core.infrastructure.container.service_descriptor import ServiceDescriptor

IT = TypeVar('IT')

class ServiceCollection:
    def __init__(self):
        self.services: List[ServiceDescriptor] = []

    def add_transient(self, interface_or_type: Type[IT], implementation: Optional[Type] = None) -> None:
        if not self._check_duplication(interface_or_type):
            descriptor = ServiceDescriptor(
                interface_or_type=interface_or_type,
                implementation=implementation,
                scope=ServiceScope.TRANSIENT,
            )
            self.services.append(descriptor)
        else:
            raise AttributeError(
                f'Transient implementation for interface/type {interface_or_type.__name__} is already registered')

    def add_singleton(self, interface_or_type: Type[IT], cls: Optional[Type] = None) -> None:
        if not self._check_duplication(interface_or_type):
            descriptor = ServiceDescriptor(
                interface_or_type=interface_or_type,
                implementation=cls,
                scope=ServiceScope.SINGLETON
            )
            self.services.append(descriptor)
        else:
            raise AttributeError(f'Singleton for interface/type {interface_or_type.__name__} is already registered')

    def _check_duplication(self, interface_or_type: Type) -> bool:
        keys = list(map(lambda service: service.interface_or_type, self.services))
        return interface_or_type in keys