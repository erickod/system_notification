from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional


@dataclass
class NotificationTarget:
    _type: str
    _target: str

    @property
    def type(self) -> str:
        return self._type.lower()

    @property
    def target(self) -> str:
        return self._target.lower()

    def __str__(self) -> str:
        return f"{self.type}:{self.target}"
