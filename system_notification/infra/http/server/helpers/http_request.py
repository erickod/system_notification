from collections import UserDict
from dataclasses import dataclass, field
from typing import Any, Dict, Mapping


class InsensitiveCaseDict(UserDict):
    def __getitem__(self, key: Any) -> Any:
        if type(key) is str:
            return super().__getitem__(key.lower())
        return super().__getitem__(key)

    def __setitem__(self, key: Any, item: Any) -> Any:
        if type(key) is str:
            self.data[key.lower()] = item
        self.data[key] = item


@dataclass
class HttpRequest:
    headers: Mapping[str, Any] = field(default_factory=dict)
    body: Dict[str, Any] = field(default_factory=dict)
    params: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.headers = InsensitiveCaseDict(**self.headers)
