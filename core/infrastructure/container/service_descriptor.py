from dataclasses import dataclass
from typing import Type, Optional, TypeVar

from core.infrastructure.container.service_scope import ServiceScope

IT = TypeVar('IT')
CT = TypeVar('CT')

@dataclass
class ServiceDescriptor:
    interface_or_type: Type[IT]
    implementation: Optional[Type[CT]]
    scope: ServiceScope
