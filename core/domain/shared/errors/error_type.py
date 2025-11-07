from enum import Enum


class ErrorType(Enum):
    NotFound = 'NotFound'
    Failure = 'Failure'
    Unexpected = 'Unexpected'
    Validation = 'Validation'
    Conflict = 'Conflict'
    InvariantViolation = 'Invariant Violation'
    Unauthorized = 'Unauthorized'
    Forbidden = 'Forbidden'
    Custom = 'Custom'
    NONE = 'No error'