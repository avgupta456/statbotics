from typing import Any, Dict


class APIModel:
    def to_dict(self) -> Dict[str, Any]:
        return {
            k: getattr(self, k).to_dict()  # type: ignore
            if isinstance(getattr(self, k), APIModel)  # type: ignore
            else getattr(self, k)  # type: ignore
            for k in self.__slots__  # type: ignore
        }
