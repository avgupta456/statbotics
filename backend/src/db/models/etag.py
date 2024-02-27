from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column

from src.db.main import Base
from src.db.models.main import Model, ModelORM, generate_attr_class
from src.db.models.types import MI, MOS, MS


class ETagORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "etags"
    year: MI = mapped_column(Integer, index=True)
    path: MS = mapped_column(String, index=True, primary_key=True)
    etag: MOS = mapped_column(String)


_ETag = generate_attr_class("ETag", ETagORM)


class ETag(_ETag, Model):
    def pk(self: "ETag") -> str:
        return self.path

    def __hash__(self: "ETag") -> int:
        return hash(self.pk())
