from typing import Any, Dict, Optional

import attr
from sqlalchemy import Column, String
from sqlalchemy.sql.schema import PrimaryKeyConstraint

from src.db.main import Base
from src.db.models.main import Model, ModelORM


class ETagORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "etags"
    path = Column(String, index=True)

    PrimaryKeyConstraint(path)

    etag = Column(String)


@attr.s(auto_attribs=True, slots=True)
class ETag(Model):
    path: str
    etag: Optional[str] = None

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "ETag":
        dict = {k: dict.get(k, None) for k in cls.__slots__}  # type: ignore
        return ETag(**dict)
