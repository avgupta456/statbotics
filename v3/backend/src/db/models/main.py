from typing import TypeVar


class ModelORM:
    pass


class Model:
    def __str__(self):
        return self.__repr__()


TModelORM = TypeVar("TModelORM", bound=ModelORM)
TModel = TypeVar("TModel", bound=Model)

# TODO: validate consistent fields, headers between all ORM/attrs models
# TODO: automatically convert sqlalchemy model to attrs model
# TODO: enforce consistent usage of playoff vs. elims
# TODO: enforce consistent usage of foul vs fouls
