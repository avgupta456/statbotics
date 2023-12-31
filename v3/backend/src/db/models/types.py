from typing import Any, Optional

from sqlalchemy.orm import Mapped

MF = Mapped[float]
MOF = Mapped[Optional[float]]

MI = Mapped[int]
MOI = Mapped[Optional[int]]

MB = Mapped[bool]
MOB = Mapped[Optional[bool]]

MS = Mapped[str]
MOS = Mapped[Optional[str]]


def values_callable(x: Any) -> Any:
    return [e.value for e in x]
