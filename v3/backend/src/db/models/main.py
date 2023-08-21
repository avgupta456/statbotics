from typing import Any, Dict, Type, TypeVar

import attr
from sqlalchemy import inspect


class ModelORM:
    pass


class Model:
    T1 = TypeVar("T1")

    # TODO: delete this
    @classmethod
    def from_dict(cls: Type[T1], dict: Dict[str, Any]) -> T1:
        dict = {k: dict.get(k, None) for k in cls.__slots__}  # type: ignore
        return cls(**dict)

    def to_dict(self) -> Dict[str, Any]:
        return attr.asdict(self)

    def sort(self) -> Any:
        raise NotImplementedError()

    def pk(self) -> str:
        raise NotImplementedError()

    def __str__(self):
        return self.__repr__()


T2 = TypeVar("T2", bound=ModelORM)


def generate_attr_class(name: str, sqlalchemy_model: Type[T2]) -> Type[T2]:
    columns = inspect(sqlalchemy_model).columns  # type: ignore
    fields = {column.name: attr.ib() for column in columns}

    out_class = attr.make_class(
        name, attrs=fields, bases=(Model,), auto_attribs=True, slots=True
    )

    return out_class  # type: ignore


TModelORM = TypeVar("TModelORM", bound=ModelORM)
TModel = TypeVar("TModel", bound=Model)


# TODO: enforce consistent usage of playoff vs. elims
# TODO: enforce consistent usage of foul vs fouls
