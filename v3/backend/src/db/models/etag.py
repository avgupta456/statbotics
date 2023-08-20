from typing import Any, Dict, Optional

from sqlalchemy import Column, Integer, String  # type: ignore
from sqlalchemy.sql.schema import PrimaryKeyConstraint  # type: ignore

from src.db.main import Base
from src.db.models.main import ModelORM, generate_attr_class


class ETagORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "etags"
    year: int = Column(Integer, index=True)
    path: str = Column(String, index=True)

    PrimaryKeyConstraint(path)

    etag: Optional[str] = Column(String)


_ETag = generate_attr_class("ETag", ETagORM)


class ETag(_ETag):
    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "ETag":
        dict = {k: dict.get(k, None) for k in cls.__slots__}  # type: ignore
        return ETag(**dict)
