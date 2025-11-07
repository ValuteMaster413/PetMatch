# https://enterprisecraftsmanship.com/posts/functional-c-handling-failures-input-errors/
from typing import TypeVar, Generic, Optional, Callable, Any, cast, List

from core.domain.shared.errors.error import Error

T = TypeVar('T')
Tin = TypeVar('Tin')
Tout = TypeVar('Tout')
Taction = TypeVar('Taction')

class Result(Generic[T]):
    def __init__(self, success: bool, content: Optional[T], error: Optional[Error]):
        self.success: bool = success
        self.error: Optional[Error] = error
        self.content: Optional[T] = content

    @property
    def failure(self) -> bool:
        return not self.success

    @classmethod
    def fail(cls, error: Error) -> 'Result[T]':
        """
        Class factory method to return new failure Result[T] objects with provided Error (required)
        """
        return cls(False, content=None, error=error)

    @classmethod
    def ok(cls, content: Optional[T] = None) -> 'Result[T]':
        """
        Class factory method to return new success Result[T] objects with provided content of type T or None
        """
        return cls(True, content=content, error=None)

    @staticmethod
    def create(value: T, error: Error = Error.NullValue()) -> 'Result[T]':
        return Result.ok(value) if value is not None else Result.fail(error=error)

    def ensure(self, predicate: Callable[[T], bool], error: Error) -> 'Result[T]':
        """
        Method to chain several Result objects and check is some predicate function applied to self.content return sTrue or False.

        Parameters
        ----------
        predicate : Callable[[T], bool]
            Callable (function) of one argument of type T return bool. It is a condition we want to check.
        error : Error
            Error object we want to be assigned to failure Result if check failed.

        Returns
        -------
        Result[T]
            'Result[T]' object:
            - Success if input result was successful initially and condition passed
            - Failure if initial result was failure
            - Failure if input result was successful but condition check failed

        """
        if self.failure:
            return self

        if predicate(self.content):
            return self

        return Result.fail(error)

    def map(self, mapping_function: Callable[[T], Tout]) -> 'Result[Tout]':
        """
        Method to transform content of type T of successful Result (self) into either:
            - another successful Result with transformed content of type Tout; or
            - failure Result of type Tout with the error came from initial Result object
        Difference with Bind: mapping_function do not return Result itself.

        """
        return Result.ok(content=mapping_function(self.content)) if self.success else Result.fail(error=self.error)

    def bind(self, bind_function: Callable[[T], 'Result[Tout]']) -> 'Result[Tout]':
        """
        Method to:
            - execute some action 'bind_function' with successful 'self' content and return new Result with content of type 'Tout'; or
            - return new failure result of type 'Tout' if initial result was failure.
        Difference with Map: bind_function returns Result object by design

        """
        if self.failure:
            return cast(Result[Tout], Result.fail(self.error))
        return bind_function(self.content)

    def match(self,
              on_success: Callable[[T], Taction],
              on_failure: Callable[['Result[T]'], Taction]
              ) -> Any:
        return on_success(self.content) if self.success else on_failure(self)

    def tap(self, action: Callable[[T], None]) -> 'Result[T]':
        """
        Method to execute 'side effect' function 'action' (return None strictly) with self.content. Returns 'self' again
        """
        if self.success:
            action(self.content)

        return self

    def side(self, action: Callable[[T], 'Result[None]']) -> 'Result[T]':
        """
        Method to execute 'side action' which notoriously return Result object without content.
        If result of 'action' is success, method returns self.
        Otherwise, it returns failure result of 'action'
        Method is intended to execute several side actions with the same initial content without switching to 'bind' result
        """
        if self.success:
            res = action(self.content)
            if res.success:
                return self
            else:
                return Result.fail(res.error)
        else:
            return self

    @staticmethod
    def combine(results: List['Result']) -> 'Result[T]':
        """
        Method to combine several Results:
            - If any of results is failure -> take the first not None error and return new failure Result with this error
            - Otherwise (if all results are successful) return Result.ok with the Tuple of results' contents
        """
        if any([x.failure for x in results]):
            """ If any of results is failure -> take the first not None error"""
            # return Result.fail(list(set([x.error for x in results if x.error is not None]))[0])
            return Result.fail([x.error for x in results if x.error is not None][0])
        """ Otherwise (if all results are successful) return Result.ok with the Tuple of results' contents """
        return Result.ok(tuple(x.content for x in results))

    def __str__(self):
        if self.success:
            return f'[Success]'
        else:
            return f'[Failure] "{self.error}"'

    def __repr__(self):
        if self.success:
            return f"<Result success={self.success}>"
        else:
            return f'<Result success={self.success}, message="{self.error}">'