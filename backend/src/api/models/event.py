import attr

from src.api.models.main import APIModel


@attr.s(auto_attribs=True, slots=True)
class APIEvent(APIModel):
    event_name: str
    year: int
