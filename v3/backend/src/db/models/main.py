from sqlalchemy import inspect, String, Integer, Float, Boolean  # type: ignore
from sqlalchemy.sql.type_api import TypeEngine  # type: ignore
import attr

from typing import Any, TypeVar, Type


class ModelORM:
    pass


class Model:
    def __str__(self):
        return self.__repr__()


T = TypeVar("T", bound=ModelORM)


def generate_attr_class(name: str, sqlalchemy_model: T) -> T:
    def sqlalchemy_to_python_type(sa_type: Type[TypeEngine]) -> type:
        if isinstance(sa_type, String):
            return str
        elif isinstance(sa_type, Integer):
            return int
        elif isinstance(sa_type, Float):
            return float
        elif isinstance(sa_type, Boolean):
            return bool

        return Any

    fields = {}
    for column in inspect(sqlalchemy_model).columns:  # type: ignore
        python_type = sqlalchemy_to_python_type(column.type)  # type: ignore
        fields[column.name] = attr.ib(type=python_type)  # type: ignore

    return attr.make_class(name, fields, bases=(Model,), auto_attribs=True, slots=True)  # type: ignore


TModelORM = TypeVar("TModelORM", bound=ModelORM)
TModel = TypeVar("TModel", bound=Model)

# TODO: enforce consistent usage of playoff vs. elims
# TODO: enforce consistent usage of foul vs fouls
