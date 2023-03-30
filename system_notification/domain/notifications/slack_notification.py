from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from system_notification.domain.notifications.base_notification import BaseNotification
from system_notification.domain.notifications.notification_target import (
    NotificationTarget,
)


class SlackNotification:
    def __init__(
        self, title: str, content: str, priority: Literal[0, 1, 2, 3] = 0
    ) -> None:
        self._notification: BaseNotification = BaseNotification(
            title, content, priority
        )

    def mark_as_sent(self) -> None:
        self._notification._is_sent = True

    def set_vars(self, vars: Dict[str, str]) -> None:
        self._notification._vars = vars

    def get_text(self, apply_vars: bool = True) -> str:
        return self._notification.get_text(apply_vars=apply_vars)

    def add_target(self, target: str) -> None:
        notification_target = NotificationTarget("slack_channel", str(target))
        self._notification._target = notification_target

    @property
    def target(self) -> Optional[NotificationTarget]:
        return self._notification._target

    @property
    def is_sent(self) -> bool:
        return self._notification._is_sent

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
        return deepcopy(self._notification._vars)

    @property
    def title(self) -> str:
        return self._notification.title

    @property
    def content(self) -> str:
        return self._notification.content

    @property
    def priority(self) -> Literal[0, 1, 2, 3]:
        return self._notification.priority

    def __contains__(self, other: Any) -> bool:
        return other == self._notification._target
