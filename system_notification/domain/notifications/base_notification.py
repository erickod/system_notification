from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, TypeVar

from system_notification.domain.notifications.notification_target import (
    NotificationTarget,
)

T = TypeVar("T", covariant=True)


@dataclass
class BaseNotification:
    title: str
    content: str
    priority: Literal[0, 1, 2, 3] = 0
    icon: str = ""

    def __post_init__(self) -> None:
        self._is_sent: bool = False
        self._vars: Dict[str, str] = {}
        self._target: Optional[NotificationTarget] = None
        self._status: str = "filled"
        if not self.priority or type(self.priority) != int:
            self.priority = 0

    def mark_as_sent(self) -> None:
        self._is_sent = True

    def set_vars(self, vars: Dict[str, str]) -> None:
        self._vars = vars
        self.title = self.title.format(**self.vars)

    def get_text(self, apply_vars: bool = True) -> str:
        if self.vars and apply_vars:
            return self.content.format(**self.vars)
        return self.content

    def add_target(self, target: NotificationTarget) -> None:
        self._target = target

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, status: str) -> None:
        if status.lower() in ("queued", "sent"):
            self._is_sent = True
        self._status = status

    @property
    def target(self) -> Optional[NotificationTarget]:
        return self._target

    @property
    def is_sent(self) -> bool:
        return self._is_sent

    @property
    def is_scheduled(self) -> bool:
        raise NotImplementedError

    def can_be_sent_at(self, date: datetime) -> bool:
        raise NotImplementedError

    def get_targets(self) -> List[str]:
        raise NotImplementedError

    def is_scheduled_to(self, date: datetime) -> bool:
        raise NotImplementedError

    def schedule(self, date: datetime) -> bool:
        raise NotImplementedError

    @property
    def vars(self) -> Dict[str, str]:
        return deepcopy(self._vars)

    def __contains__(self, other: Any) -> bool:
        return other == self._target
