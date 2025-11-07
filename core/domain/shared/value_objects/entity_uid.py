import uuid
from typing import Optional, TypeVar, Type

from core.domain.shared.meta import NoPublicConstructor
from core.domain.shared.abstractions.value_object import ValueObject
from core.domain.shared.errors.error import Error
from core.domain.shared.result import Result

T = TypeVar("T")

class EntityUID(ValueObject, metaclass=NoPublicConstructor):
    def __init__(self, value: str):
        self._value = value

    @property
    def value(self):
        return self._value

    @classmethod
    def create(cls: Type[T], value: Optional[str]=None) -> Result[T]:
        if not value:
            value = uuid.uuid4().hex
            return Result.ok(cls._create(value))
        else:
            if len(value.strip())>32:
                return Result.fail(Error.Validation(
                    code="invalid.uid",
                    message=f"invalid uid: {value}",
                ))
            else:
                return Result.ok(cls._create(value.strip()))

    def __eq__(self, other):
        if isinstance(other, EntityUID):
            return vars(self) == vars(other)
        return False

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return str(f'{self.__class__.__name__}[{self.value}]')

    def __str__(self):
        return str(f'{self.__class__.__name__}[{self.value}]')

