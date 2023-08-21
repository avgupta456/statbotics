from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column

from src.db.main import Base
from src.db.models.main import ModelORM, Model, generate_attr_class
from src.db.models.types import MI, MS, MOS


class ETagORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "etags"
    year: MI = mapped_column(Integer, index=True)
    path: MS = mapped_column(String, index=True, primary_key=True)
    etag: MOS = mapped_column(String)


_ETag = generate_attr_class("ETag", ETagORM)


class ETag(_ETag, Model):
    def pk(self: "ETag") -> str:
        return f"{self.year}-{self.path}"
