from typing import Any, List, Optional, TypeVar

from src.db.models.main import Model, ModelORM

T = TypeVar("T")


def common_filters(
    model_orm: ModelORM,
    model: Model,
    metric: Optional[str],
    ascending: Optional[bool],
    limit: Optional[int],
    offset: Optional[int],
) -> Any:
    def decorator(func: Any) -> Any:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            data = func(*args, **kwargs)

            if metric is not None:
                data = data.filter(model_orm.__dict__[metric] != None)  # type: ignore  # noqa: E711
                if ascending is not None and ascending:
                    data = data.order_by(model_orm.__dict__[metric].asc())  # type: ignore
                else:
                    data = data.order_by(model_orm.__dict__[metric].desc())  # type: ignore
            if limit is not None:
                data = data.limit(limit)  # type: ignore
            if offset is not None:
                data = data.offset(offset)  # type: ignore
            out_data: List[model_orm] = data.all()  # type: ignore

            return [model.from_dict(x.__dict__) for x in out_data]  # type: ignore

        return wrapper

    return decorator
