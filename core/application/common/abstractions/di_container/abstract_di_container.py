from abc import ABC, abstractmethod
from typing import Type, TypeVar, Optional

IT = TypeVar('IT')
CT = TypeVar('CT')
T = TypeVar('T')

class AbstractDIContainer(ABC):
    @abstractmethod
    def get_required(self, cls: type(T)) -> T:
        ...
    @abstractmethod
    def add_transient(self, interface_or_type: Type[IT], implementation: Optional[Type[CT]] = None) -> None:
        ...
    @abstractmethod
    def add_singleton(self, interface_or_type: Type[IT], cls: Optional[Type[CT]] = None) -> None:
        ...

    @abstractmethod
    def is_singleton_implementation(self, interface: Type[T]) -> bool:
        ...

    @abstractmethod
    def is_transient_implementation(self, interface: Type[T]) -> bool:
        ...
