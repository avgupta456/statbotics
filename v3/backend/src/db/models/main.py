from typing import Any, Dict, Type, TypeVar

import attr
from sqlalchemy import inspect


class ModelORM:
    __table__: Any


class Model:
    T1 = TypeVar("T1")

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

    def __hash__(self) -> int:
        return hash(self.pk())

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Model):
            return False
        return self.pk() == other.pk()

    def __str__(self):
        return self.__repr__()


T2 = TypeVar("T2", bound=ModelORM)


def generate_attr_class(name: str, sqlalchemy_model: Type[T2]) -> Type[T2]:
    columns = inspect(sqlalchemy_model).columns  # type: ignore

    fields = {
        c.name: attr.ib(default=None if c.default is None else c.default.arg)
        for c in columns
    }

    return attr.make_class(  # type: ignore
        name, attrs=fields, bases=(Model,), auto_attribs=True, slots=True
    )


TModelORM = TypeVar("TModelORM", bound=ModelORM)
TModel = TypeVar("TModel", bound=Model)
