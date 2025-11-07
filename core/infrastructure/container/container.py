import inspect
from typing import TypeVar, Type, Dict, Optional

from core.application.common.abstractions.di_container.abstract_di_container import AbstractDIContainer

IT = TypeVar('IT')
CT = TypeVar('CT')
T = TypeVar('T')

class DependencyInjectionContainer(AbstractDIContainer):
    def __init__(self):
        self._transient_implementations: Dict[Type[IT], Type[CT]] = {}
        self._singleton_implementations: Dict[Type[T], T] = {AbstractDIContainer: self}

    def get_required(self, cls: type(T)) -> T:
        return self._get(cls)

    def _get(self, cls: type(T)) -> T:
        if cls in self._singleton_implementations.keys():
            return self._singleton_implementations[cls]

        # Check if cls is an interface and already in list
        if cls in self._transient_implementations.keys():
            concrete_cls = self._transient_implementations.get(cls)
            return self._get(concrete_cls)

        init_signature = inspect.signature(cls.__init__)
        init_args_kwargs = init_signature.parameters
        # Check if some other deps needed to instantiate
        num_params = sum(1 for param in init_args_kwargs.values()
                         if param.kind not in (inspect.Parameter.VAR_POSITIONAL,
                                               inspect.Parameter.VAR_KEYWORD))
        if num_params == 1:
            if cls.__base__.__name__ == 'ABC':
                raise AttributeError(f'No implementation for interface/type {cls.__name__} is registered')
            else:
                try:
                    instance = cls()
                    return instance
                except TypeError:
                    raise AttributeError(f'No implementation for interface/type {cls.__name__} is registered')
        else:
            init_arguments = {}
            for parameter_name, parameter in init_args_kwargs.items():
                if parameter_name != 'self':
                    init_arguments[parameter_name] = self._get(parameter.annotation)
            return cls(**init_arguments)

    def add_transient(self, interface_or_type: Type[IT], implementation: Optional[Type[CT]] = None) -> None:
        """
        Method to add transients.
        If 'interface_or_type' is not already registered (else raise error):
            Check if implementation provided (not None). If so: put it as a value into collection.
            Otherwise, value is 'interface_or_type'.
            In both cases key is 'interface_or_type'

        """
        if not interface_or_type in self._transient_implementations.keys():
            if implementation is None:
                self._transient_implementations[interface_or_type] = interface_or_type
            else:
                self._transient_implementations[interface_or_type] = implementation
        else:
            raise AttributeError(
                f'Transient implementation for interface/type {interface_or_type.__name__} is already registered')

    def add_singleton(self, interface_or_type: Type[IT], cls: Optional[Type[CT]] = None) -> None:
        """
        Method to add singleton. Takes 'interface_or_type' as Type object and optional 'cls' concrete class.
        If 'cls' (concrete class) is not provided, 'interface_or_type' is assumed as type.
        If 'interface_or_type' is not already registered (else raise error):
            Check if concrete class is None (not provided):
                If so: instantiate instance of provided 'interface_or_type' by calling _get() method
                Resulting instance put into collection as a value, when key is 'interface_or_type'
            If concrete class ('cls') is provided:
                Instantiate instance by calling _get() of provided 'cls'
                Resulting instance put into collection as a value, when key is 'interface_or_type'
        """
        if not interface_or_type in self._singleton_implementations.keys():
            if cls is None:
                instance = self._get(interface_or_type)
                self._singleton_implementations[interface_or_type] = instance
            else:
                instance = self._get(cls)
                self._singleton_implementations[interface_or_type] = instance
        else:
            raise AttributeError(f'Singleton for interface/type {interface_or_type.__name__} is already registered')

    def is_singleton_implementation(self, interface: Type[IT]) -> bool:
        return interface in self._singleton_implementations.keys()

    def is_transient_implementation(self, interface: Type[IT]) -> bool:
        return interface in self._transient_implementations.keys()


