# https://enterprisecraftsmanship.com/posts/error-handling-exception-or-result/
# https://enterprisecraftsmanship.com/posts/advanced-error-handling-techniques/

from dataclasses import dataclass
from typing import Optional, Dict

from core.domain.shared.abstractions.value_object import ValueObject
from core.domain.shared.errors.error_type import ErrorType


@dataclass(frozen=True)
class Error(ValueObject):
    code: str
    type: ErrorType
    message: str = ''
    metadata: Optional[Dict[str, str]] = None

    @property
    def none(self) -> 'Error':
        return Error('', ErrorType.NONE)

    def add_meta(self, message: str) -> 'Error':
        if not self.metadata:
            return Error(self.code, self.type, self.message, {'extensions': message})
        self.metadata['extensions'] = message
        return self

    @staticmethod
    def Failure(code: str, message: str, metadata: Optional[Dict[str, str]]=None) -> 'Error':
        return Error(code, ErrorType.Failure, message, metadata)

    @staticmethod
    def Unexpected(code: str, message: str, metadata: Optional[Dict[str, str]]=None) -> 'Error':
        return Error(code, ErrorType.Unexpected, message, metadata)

    @staticmethod
    def Validation(code: str, message: str, metadata: Optional[Dict[str, str]]=None) -> 'Error':
        return Error(code, ErrorType.Validation, message, metadata)

    @staticmethod
    def Conflict(code: str, message: str, metadata: Optional[Dict[str, str]]=None) -> 'Error':
        return Error(code, ErrorType.Conflict, message, metadata)

    @staticmethod
    def NotFound(code: str, message: str, metadata: Optional[Dict[str, str]]=None) -> 'Error':
        return Error(code, ErrorType.NotFound, message, metadata)

    @staticmethod
    def InvariantViolation(code: str, message: str, metadata: Optional[Dict[str, str]]=None) -> 'Error':
        return Error(code, ErrorType.InvariantViolation, message, metadata)

    @staticmethod
    def Unauthorized(code: str, message: str, metadata: Optional[Dict[str, str]]=None) -> 'Error':
        return Error(code, ErrorType.Unauthorized, message, metadata)

    @staticmethod
    def Forbidden(code: str, message: str, metadata: Optional[Dict[str, str]]=None) -> 'Error':
        return Error(code, ErrorType.Forbidden, message, metadata)

    @staticmethod
    def Custom(code: str, message: str, metadata: Optional[Dict[str, str]]=None) -> 'Error':
        return Error(code, ErrorType.Custom, message, metadata)

    @staticmethod
    def NullValue() -> 'Error':
        return Error('error.null.value.provided', ErrorType.NotFound, 'Provided value is None')

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.code == other.code
        else:
            raise TypeError(f"Can not compare Error object with another type {other.__class__.__name__}")

    def __repr__(self):
        return f'''Error.{self.type.value}[
        code='{self.code}',
        message='{self.message}',
        metadata={self.metadata or ''}]
        '''

# e=Error.Forbidden('invalid.subscription', 'This core product is not available for the client')
# print(str(e))

