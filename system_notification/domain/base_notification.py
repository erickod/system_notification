from dataclasses import dataclass
from typing import Literal


@dataclass
class BaseNotification:
    title: str
    content: str
    priority: Literal[0, 1, 2, 3] = 0

    def __post_init__(self) -> None:
        self._is_sent: bool = False
        if not self.priority:
            self.priority = 0
        if type(self.priority) != int:
            self.priority = 0

    def mark_as_sent(self) -> None:
        self._is_sent = True

    @property
    def is_sent(self) -> bool:
        return self._is_sent

    @property
    def is_scheduled(self) -> bool:
        raise NotImplementedError
