from typing import TypeVar


class ModelORM:
    pass


class Model:
    def __str__(self):
        return self.__repr__()


TModelORM = TypeVar("TModelORM", bound=ModelORM)
TModel = TypeVar("TModel", bound=Model)
