import json
from abc import ABC
from dataclasses import dataclass, fields
from typing import Tuple, Optional, List, TypeVar, Type, Dict, Any, ForwardRef

T = TypeVar('T', bound='AbstractQueryResponse')

@dataclass
class AbstractQueryResponse(ABC):

    @classmethod
    def attrs(cls, exclude: Optional[List[str]] = None) -> Tuple:
        return AbstractQueryResponse._attrs(cls, exclude)

    @staticmethod
    def _attrs(cls, exclude: Optional[List[str]] = None) -> Tuple:
        if exclude:
            return tuple(map(lambda x: x.name, filter(lambda y: y.name not in exclude, fields(cls))))
        return tuple(map(lambda x: x.name, fields(cls)))

    @classmethod
    def from_json(cls: Type[T], string: str) -> T:
        return AbstractQueryResponse.from_dict(cls, json.loads(string))

    @staticmethod
    def from_dict(cls: Type[T], data: Dict[str, Any], mentioned_types: Optional[List[Type]] = None) -> Any:
        init_args = {}
        if mentioned_types is None:
            mentioned_types = [cls]

        for field in fields(cls):
            # attr_value = data[field.name]
            attr_data_type = type(data[field.name]) if field.name in data else None
            if attr_data_type == dict:
                attr_field_type = field.type
                if type(attr_field_type) == str:
                    init_args[field.name] = AbstractQueryResponse.from_dict(
                        getattr(mentioned_types[0], attr_field_type.split('.')[-1]),
                        data[field.name], mentioned_types
                    )
                else:
                    attr_field_type = attr_field_type.__args__[0]
                    if type(attr_field_type) == ForwardRef:
                        attr_field_type = attr_field_type.__forward_arg__
                    init_args[field.name] = AbstractQueryResponse.from_dict(
                        getattr(mentioned_types[0], attr_field_type.split('.')[-1]),
                        data[field.name],
                        mentioned_types
                    )
            elif attr_data_type == list:
                attr_field_type = field.type.__args__[0]
                if type(attr_field_type) == ForwardRef:
                    attr_field_type = attr_field_type.__forward_arg__
                init_args[field.name] = [
                    AbstractQueryResponse.from_dict(
                        getattr(mentioned_types[0], attr_field_type.split('.')[-1]),
                        x,
                        mentioned_types) for x in data[field.name]
                ]
            else:
                init_args[field.name] = data[field.name] if field.name in data else None

        return cls(**init_args)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        outer_attrs = vars(cls)
        if any(isinstance(attr_value, type) for attr_value in outer_attrs.values()):
            nested_classes = [value for value in outer_attrs.values() if isinstance(value, type)]
            for nested_cls in nested_classes:
                setattr(nested_cls, 'attrs', classmethod(AbstractQueryResponse._attrs))